import yfinance as yf

def fetch_live_data(symbol, period="7d", interval="5m"):
    """
    Fetch sufficient data for indicators
    """
    ticker = yf.Ticker(symbol)
    data = ticker.history(period=period, interval=interval)

    if data is None or data.empty:
        raise ValueError("No market data available")

    return data
