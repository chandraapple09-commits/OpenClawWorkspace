import yfinance as yf
import numpy as np

def trend_prediction(symbol: str) -> str:
    try:
        df = yf.download(symbol, period="3mo", interval="1d", progress=False)

        if df.empty or len(df) < 20:
            return "⚠️ Insufficient data"

        close = df["Close"].dropna()
        x = np.arange(len(close))
        y = close.values

        slope = np.polyfit(x, y, 1)[0]

        if slope > 0:
            return "📈 BULLISH"
        elif slope < 0:
            return "📉 BEARISH"
        else:
            return "➡️ SIDEWAYS"

    except Exception as e:
        return "⚠️ Trend unavailable"

