import yfinance as yf
import matplotlib.pyplot as plt
from pathlib import Path

CHART_DIR = Path("data/charts")
CHART_DIR.mkdir(parents=True, exist_ok=True)

def generate_price_chart(symbol: str) -> str:
    df = yf.download(symbol, period="3mo", interval="1d", progress=False)

    if df.empty:
        return None

    plt.figure(figsize=(8, 4))
    plt.plot(df.index, df["Close"], label="Close Price")
    plt.title(f"{symbol} - Last 3 Months")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.legend()

    file_path = CHART_DIR / f"{symbol}.png"
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()

    return str(file_path)

