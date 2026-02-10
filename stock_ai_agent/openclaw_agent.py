from agents.market_analyst.agent import run_market_agent
from stock_registry import is_valid_stock
import numpy as np

def safe(v):
    if isinstance(v, (np.float32, np.float64)):
        return float(v)
    return v

def handle_stock_query(symbol: str) -> str:
    symbol = symbol.upper()

    if not is_valid_stock(symbol):
        return (
            "❌ Invalid stock symbol.\n\n"
            "Try:\n"
            "/stock RELIANCE.NS\n"
            "/search TATA"
        )

    try:
        result = run_market_agent(symbol)

        stock = str(result.get("Stock", symbol))
        price = safe(result.get("Last Price", "N/A"))
        prob = safe(result.get("Hike Probability (%)", "N/A"))
        outlook = str(result.get("Outlook", "N/A"))

        return (
            f"📊 {stock}\n"
            f"Last Price: ₹{price}\n"
            f"Hike Probability: {prob}%\n"
            f"Outlook: {outlook}"
        )

    except Exception as e:
        return f"❌ Error fetching stock data:\n{e}"

