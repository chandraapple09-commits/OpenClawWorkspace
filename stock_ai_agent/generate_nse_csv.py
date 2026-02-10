import pandas as pd
from pathlib import Path

# Output directory
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

OUT_FILE = DATA_DIR / "indian_stocks.csv"

# Official NSE equity list
URL = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"

print("⬇️ Downloading NSE equity list...")
df = pd.read_csv(URL)

print("🧹 Cleaning data...")
df = df[["SYMBOL", "NAME OF COMPANY"]].dropna()

# Convert to Yahoo Finance NSE symbols
df["symbol"] = df["SYMBOL"].str.upper() + ".NS"
df["name"] = df["NAME OF COMPANY"].str.title()

final_df = df[["symbol", "name"]]

print(f"💾 Writing {len(final_df)} stocks to CSV...")
final_df.to_csv(OUT_FILE, index=False)

print("✅ DONE!")
print(f"📁 Saved to: {OUT_FILE}")

