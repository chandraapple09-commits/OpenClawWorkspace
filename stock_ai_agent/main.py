import os
import logging
import yfinance as yf
import asyncio

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("token")

logging.basicConfig(level=logging.INFO)

print("BOT STARTED")

# ---------------- FETCH STOCK ---------------- #

def get_price(symbol):

    symbol = symbol.upper()

    try:
        # NSE
        ticker = yf.Ticker(symbol + ".NS")
        data = ticker.history(period="1d", timeout=10)

        if not data.empty:
            return f"₹ {round(data['Close'].iloc[-1],2)} (NSE)"

        # US fallback
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d", timeout=10)

        if not data.empty:
            return f"$ {round(data['Close'].iloc[-1],2)} (US)"

        return None

    except Exception as e:
        print("FETCH ERROR:", e)
        return "ERROR"


# ---------------- COMMANDS ---------------- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📈 Stock Bot Online\n\nUse:\n/price TCS"
    )


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Usage: /price TCS")
        return

    symbol = context.args[0]

    msg = await update.message.reply_text("Fetching price...")

    result = get_price(symbol)

    if result == "ERROR":
        await msg.edit_text("API Error. Try later.")
        return

    if result is None:
        await msg.edit_text("Stock not found")
        return

    await msg.edit_text(f"{symbol.upper()} → {result}")


# ---------------- MAIN ---------------- #

async def main():

    if not TOKEN:
        raise ValueError("BOT_TOKEN missing in Railway variables")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))

    print("BOT RUNNING")

    await app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
