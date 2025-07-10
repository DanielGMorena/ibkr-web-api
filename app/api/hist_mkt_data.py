import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.ib import IBClientManager

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/histMktData", tags=["Historical Market Data"])


@router.get("/")
async def get_hist_market_data(
    symbol: str = Query(..., description="The symbol to fetch data for"),
    duration: str = Query("1 D", description="Duration string (e.g., '1 D')"),
    bar_size: str = Query("1 min", description="Bar size (e.g., '1 min')"),
    what_to_show: str = Query("TRADES", description="What to show (e.g., 'TRADES')"),
    use_rth: int = Query(
        1, ge=0, le=1, description="Use Regular Trading Hours (0 or 1)"
    ),
    end_datetime: Optional[str] = Query(
        None,
        description="Optional end datetime in IB format (e.g., '20240710 14:00:00') or '' for now",
    ),
):
    """
    Handle GET request to fetch historical market data asynchronously.
    """
    logger.info(
        "Historical data request: "
        f"symbol={symbol}, duration={duration}, bar_size={bar_size}, "
        f"what_to_show={what_to_show}, use_rth={use_rth}, end_datetime={end_datetime}"
    )

    try:
        async with IBClientManager() as ib:
            contract_details = await ib.reqContractDetailsAsync(symbol)
            if not contract_details:
                raise HTTPException(
                    status_code=404, detail=f"No contract found for symbol '{symbol}'"
                )

            qualified_contracts = await ib.qualifyContractsAsync(
                contract_details[0].contract
            )
            contract = qualified_contracts[0]

            bars = await ib.reqHistoricalDataAsync(
                contract,
                endDateTime=end_datetime or "",  # empty string means "now"
                durationStr=duration,
                barSizeSetting=bar_size,
                whatToShow=what_to_show,
                useRTH=use_rth,
                formatDate=1,
            )

            return [bar.__dict__ for bar in bars]

    except Exception as e:
        logger.exception("Failed to fetch historical market data")
        raise HTTPException(status_code=500, detail=str(e))
