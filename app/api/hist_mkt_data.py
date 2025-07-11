import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from ib_insync import Contract

from app.ib import IBClientManager

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/histMktData", tags=["Historical Market Data"])


@router.get("/")
async def get_hist_market_data(
    symbol: str = Query(..., description="The symbol to fetch data for"),
    duration: str = Query(
        "1 D",
        description=(
            "Duration string specifying how far back to retrieve data (default: '1 D').\n"
            "Format: <int> <unit> (e.g., '1 D', '2 W', '6 M', '1 Y')\n"
            "Valid units:\n"
            " - S: Seconds\n"
            " - D: Days\n"
            " - W: Weeks\n"
            " - M: Months\n"
            " - Y: Years"
        ),
    ),
    bar_size: str = Query(
        "1 min",
        description=(
            "Bar size for OHLCV aggregation (default: '1 min').\n"
            "Valid sizes:\n"
            " - secs: 1, 5, 10, 15, 30\n"
            " - mins: 1, 2, 3, 5, 10, 15, 20, 30\n"
            " - hours: 1, 2, 3, 4, 8\n"
            " - day: 1\n"
            " - week: 1\n"
            " - month: 1"
        ),
    ),
    what_to_show: str = Query(
        "TRADES",
        description=(
            "The type of data to request (default: 'TRADES').\n"
            "Common values include:\n"
            " - TRADES\n"
            " - BID\n"
            " - ASK\n"
            " - MIDPOINT\n"
            " - HISTORICAL_VOLATILITY\n"
            " - OPTION_IMPLIED_VOLATILITY\n"
            " - FEE_RATE\n"
            " - REBATE_RATE"
        ),
    ),
    use_rth: bool = Query(
        True,
        description="Use Regular Trading Hours only: True = RTH only, False = include extended hours",
    ),
    end_datetime: Optional[str] = Query(
        None,
        description="End datetime in IB format (e.g., '20240710 14:00:00'). Use empty or None for current time.",
    ),
) -> List[Dict[str, Any]]:
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
            contract = Contract(
                symbol=symbol, secType="STK", exchange="SMART", currency="USD"
            )
            contract_details = await ib.reqContractDetailsAsync(contract)
            if not contract_details:
                raise HTTPException(
                    status_code=404, detail=f"No contract found for symbol '{symbol}'"
                )

            if not contract_details[0].contract:
                raise HTTPException(
                    status_code=404,
                    detail=f"No valid contract found for symbol '{symbol}'",
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

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Failed to fetch historical market data")
        raise HTTPException(status_code=500, detail=str(e))
