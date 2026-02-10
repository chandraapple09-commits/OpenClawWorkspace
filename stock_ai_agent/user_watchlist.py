import json
from pathlib import Path

FILE = Path("data/user_watchlist.json")
FILE.parent.mkdir(exist_ok=True)

if FILE.exists():
    WATCHLIST = json.loads(FILE.read_text())
else:
    WATCHLIST = {}

def add(user_id: int, symbol: str):
    uid = str(user_id)
    WATCHLIST.setdefault(uid, [])
    if symbol not in WATCHLIST[uid]:
        WATCHLIST[uid].append(symbol)
        save()

def remove(user_id: int, symbol: str):
    uid = str(user_id)
    if uid in WATCHLIST and symbol in WATCHLIST[uid]:
        WATCHLIST[uid].remove(symbol)
        save()

def get(user_id: int):
    return WATCHLIST.get(str(user_id), [])

def save():
    FILE.write_text(json.dumps(WATCHLIST, indent=2))

