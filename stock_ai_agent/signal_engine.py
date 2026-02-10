from ml_trend import trend_prediction
from openclaw_agent import handle_stock_query

def generate_signal(symbol: str) -> str:
    result = handle_stock_query(symbol)

    if "HIGH HIKE" in result:
        return "🟢 BUY (High upside probability)"
    elif "MODERATE" in result:
        return "🟡 HOLD (Wait for confirmation)"
    elif "LOW HIKE" in result:
        return "🔴 SELL / AVOID (Weak outlook)"
    else:
        return "⚪ NO CLEAR SIGNAL"

