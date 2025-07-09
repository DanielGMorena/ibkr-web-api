import logging

from flask import Blueprint, jsonify, request

from app.ib import IBClientManager

logger = logging.getLogger(__name__)
hist_mkt_data_bp = Blueprint("hist_mkt_data", __name__, url_prefix="/histMktData")


@hist_mkt_data_bp.route("", methods=["GET"])
def get_hist_market_data():
    """
    Handle GET request to fetch historical market data.

    Query Parameters:
        symbol (str): The symbol to fetch data for.
        duration (str): Duration string (e.g., "1 D").
        bar_size (str): Bar size (e.g., "1 min").
        what_to_show (str): e.g., "TRADES"
        use_rth (int): 0 or 1 (use regular trading hours)

    Returns:
        JSON: Historical bars or error message.
    """
    symbol = request.args.get("symbol")
    duration = request.args.get("duration", "1 D")
    bar_size = request.args.get("bar_size", "1 min")
    what_to_show = request.args.get("what_to_show", "TRADES")
    use_rth = int(request.args.get("use_rth", 1))

    logger.info(
        "Received historical market data request: "
        f"symbol={symbol}, duration={duration}, bar_size={bar_size}, "
        f"what_to_show={what_to_show}, use_rth={use_rth}"
    )

    if not symbol:
        logger.warning("Missing required parameter 'symbol'")
        return jsonify({"error": "Missing required parameter 'symbol'"}), 400

    try:
        with IBClientManager() as ib:
            contract_details = ib.reqContractDetails(symbol)
            if not contract_details:
                logger.warning(f"No contract details found for symbol: {symbol}")
                return jsonify(
                    {"error": f"No contract found for symbol '{symbol}'"}
                ), 404

            contract = ib.qualifyContracts(contract_details[0].contract)[0]
            bars = ib.reqHistoricalData(
                contract,
                endDateTime="",
                durationStr=duration,
                barSizeSetting=bar_size,
                whatToShow=what_to_show,
                useRTH=use_rth,
                formatDate=1,
            )
            logger.info(f"Retrieved {len(bars)} bars for symbol: {symbol}")
            return jsonify([bar.__dict__ for bar in bars])

    except Exception as e:
        logger.exception("Failed to fetch historical market data")
        return jsonify({"error": str(e)}), 500
