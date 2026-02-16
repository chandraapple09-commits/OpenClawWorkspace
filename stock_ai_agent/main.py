import os
import asyncio
import logging
import yfinance as yf

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# ==============================
# CONFIG
# ==============================

TOKEN = os.getenv("8466480154:AAFwBaOlbRYkRTLzPKxVjlC4COtT94_r_TE") or "PUT_YOUR_TOKEN_HERE"

# logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

print("🚀 BOT STARTING...")
print("Running Environment:", "RAILWAY" if os.getenv("RAILWAY_ENVIRONMENT") else "LOCAL")

# ==============================
# SIMPLE DATABASE (memory)
# ==============================

user_watchlist = {}

# ==============================
# STOCK FUNCTIONS
# ==============================

def get_price(symbol: str):
    try:
        stock = yf.Ticker(symbol + ".NS")
        data = stock.history(period="1d")

        if data.empty:
            return None

        return round(data["Close"].iloc[-1], 2)

    except Exception as e:
        print("Price error:", e)
        return None


def simple_signal(price: float):
    if price > 1000:
        return "📈 Strong Stock"
    elif price > 500:
        return "📊 Stable"
    else:
        return "⚠️ Risky"


# ==============================
# COMMANDS
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Stock AI Bot Online*\n\n"
        "Commands:\n"
        "/price SYMBOL\n"
        "/add SYMBOL\n"
        "/watchlist\n"
        "/remove SYMBOL",
        parse_mode="Markdown"
    )


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /price TCS")
        return

    symbol = context.args[0].upper()

    price = get_price(symbol)

    if price is None:
        await update.message.reply_text("❌ Stock not found")
        return

    signal = simple_signal(price)

    await update.message.reply_text(
        f"📊 {symbol}\n"
        f"Price: ₹{price}\n"
        f"Signal: {signal}"
    )


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id

    if not context.args:
        await update.message.reply_text("Usage: /add TCS")
        return

    symbol = context.args[0].upper()

    user_watchlist.setdefault(user, set()).add(symbol)

    await update.message.reply_text(f"✅ Added {symbol} to watchlist")


async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id

    if not context.args:
        await update.message.reply_text("Usage: /remove TCS")
        return

    symbol = context.args[0].upper()

    if user in user_watchlist and symbol in user_watchlist[user]:
        user_watchlist[user].remove(symbol)
        await update.message.reply_text(f"❌ Removed {symbol}")
    else:
        await update.message.reply_text("Not in watchlist")


async def watchlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id

    if user not in user_watchlist or not user_watchlist[user]:
        await update.message.reply_text("Watchlist empty")
        return

    msg = "📊 Your Watchlist:\n\n"

    for sym in user_watchlist[user]:
        price = get_price(sym)
        msg += f"{sym} → ₹{price}\n"

    await update.message.reply_text(msg)


# ==============================
# ERROR HANDLER
# ==============================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print("⚠️ ERROR:", context.error)


# ==============================
# MAIN
# ==============================

async def main():

    if TOKEN == "8466480154:AAFwBaOlbRYkRTLzPKxVjlC4COtT94_r_TE":
        raise ValueError("❌ BOT TOKEN NOT SET")

    app = ApplicationBuilder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("remove", remove))
    app.add_handler(CommandHandler("watchlist", watchlist))

    # errors
    app.add_error_handler(error_handler)

    print("✅ BOT RUNNING")
    await app.run_polling(drop_pending_updates=True)


# ==============================
# RUN
# ==============================

if __name__ == "__main__":
    asyncio.run(main())
