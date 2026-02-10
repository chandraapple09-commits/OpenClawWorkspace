print("🔥 telegram_bot.py loaded (INLINE + SEARCH + WATCHLIST + CHARTS + SIGNALS)")

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import TELEGRAM_BOT_TOKEN
from openclaw_agent import handle_stock_query
from ml_trend import trend_prediction
from stock_registry import STOCKS
from user_watchlist import add as add_watch, get as get_watch
from chart_generator import generate_price_chart
from signal_engine import generate_signal


PAGE_SIZE = 5
SEARCH_MODE = set()


def build_stock_keyboard(page=0, stocks=None):
    symbols = stocks if stocks else list(STOCKS.keys())
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE

    keyboard = [[InlineKeyboardButton("🔍 Search Stock", callback_data="SEARCH")]]

    for sym in symbols[start:end]:
        keyboard.append(
            [InlineKeyboardButton(sym, callback_data=f"STOCK:{sym}")]
        )

    nav = []
    if start > 0:
        nav.append(InlineKeyboardButton("⬅ Prev", callback_data=f"PAGE:{page-1}"))
    if end < len(symbols):
        nav.append(InlineKeyboardButton("Next ➡", callback_data=f"PAGE:{page+1}"))

    if nav:
        keyboard.append(nav)

    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📈 Select a stock",
        reply_markup=build_stock_keyboard(),
    )


async def watchlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stocks = get_watch(update.effective_user.id)
    if not stocks:
        await update.message.reply_text("⭐ Watchlist is empty")
        return
    await update.message.reply_text("⭐ Watchlist:\n" + "\n".join(stocks))


async def on_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "SEARCH":
        SEARCH_MODE.add(user_id)
        await query.message.reply_text("🔍 Type stock name")
        return

    if data.startswith("PAGE:"):
        page = int(data.split(":")[1])
        await query.edit_message_reply_markup(build_stock_keyboard(page))
        return

    if data.startswith("STOCK:"):
        symbol = data.split(":")[1]

        analysis = handle_stock_query(symbol)
        trend = trend_prediction(symbol)
        signal = generate_signal(symbol)

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⭐ Watchlist", callback_data=f"WATCH:{symbol}"),
                InlineKeyboardButton("📊 Chart", callback_data=f"CHART:{symbol}")
            ]
        ])

        await query.message.reply_text(
            f"{analysis}\n\n🧠 Trend: {trend}\n📌 Signal: {signal}",
            reply_markup=keyboard
        )
        return

    if data.startswith("WATCH:"):
        symbol = data.split(":")[1]
        add_watch(user_id, symbol)
        await query.message.reply_text(f"⭐ {symbol} added to watchlist")
        return

    if data.startswith("CHART:"):
        symbol = data.split(":")[1]
        chart_path = generate_price_chart(symbol)
        if chart_path:
            await query.message.reply_photo(photo=open(chart_path, "rb"))
        else:
            await query.message.reply_text("⚠️ Chart unavailable")
        return


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in SEARCH_MODE:
        return

    SEARCH_MODE.remove(user_id)
    text = update.message.text.lower()

    matched = [
        sym for sym, name in STOCKS.items()
        if text in sym.lower() or text in name.lower()
    ]

    if not matched:
        await update.message.reply_text("❌ No match found")
        return

    await update.message.reply_text(
        "📈 Select a stock:",
        reply_markup=build_stock_keyboard(stocks=matched)
    )


def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("watchlist", watchlist))
    app.add_handler(CallbackQueryHandler(on_button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()


if __name__ == "__main__":
    main()
