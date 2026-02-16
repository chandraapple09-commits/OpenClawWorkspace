import csv
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "indian_stocks.csv"

STOCKS = {}

with open(DATA_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        symbol = (row.get("symbol") or "").strip().upper()
        name = (row.get("name") or "").strip()

        # Skip bad / empty rows
        if not symbol or not name:
            continue

        STOCKS[symbol] = name


def is_valid_stock(symbol: str) -> bool:
    return symbol.upper() in STOCKS


def search_stock(query: str):
    query = query.lower().strip()
    results = []

    for symbol, name in STOCKS.items():
        # Safe string matching
        if query in symbol.lower() or query in name.lower():
            results.append(f"{symbol} ({name})")

    return results[:10]   # limit to 10 results
