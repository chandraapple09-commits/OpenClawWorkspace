import logging
import io
import yfinance as yf
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

# ==============================================================================
# 🔐 CONFIGURATION
# ==============================================================================
# 👉 REPLACE THIS WITH YOUR NEW TOKEN
TELEGRAM_BOT_TOKEN ="8466480154:AAFwBaOlbRYkRTLzPKxVjlC4COtT94_r_TE"

STOCKS_PER_PAGE = 10
INITIAL_CAPITAL = 100000.0  # ₹1 Lakh Virtual Cash

# ==============================================================================
# 📋 MASTER STOCK LIST (150+ Top Indian Stocks)
# ==============================================================================
STOCK_LIST = [
    # --- TATA GROUP ---
    "TATAMOTORS.NS", "TATASTEEL.NS", "TCS.NS", "TITAN.NS", "TATAPOWER.NS",
    "TATAELXSI.NS", "TATACHEM.NS", "TATACONSUM.NS", "TATACOMM.NS", "VOLTAS.NS",
    "TRENT.NS", "INDIHOTEL.NS", "TATAINVEST.NS", "TTML.NS", "RALLIS.NS",

    # --- ADANI GROUP ---
    "ADANIENT.NS", "ADANIPORTS.NS", "ADANIPOWER.NS", "ADANIGREEN.NS",
    "ADANIENSOL.NS", "ATGL.NS", "AWL.NS", "ACC.NS", "AMBUJACEM.NS", "NDTV.NS",

    # --- BANKING & FINANCE ---
    "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "KOTAKBANK.NS", "AXISBANK.NS",
    "INDUSINDBK.NS", "BANKBARODA.NS", "PNB.NS", "IDFCFIRSTB.NS", "AUUBANK.NS",
    "BANDHANBNK.NS", "FEDERALBNK.NS", "BAJFINANCE.NS", "BAJAJHLDNG.NS",
    "CHOLAFIN.NS", "MUTHOOTFIN.NS", "ABCAPITAL.NS", "LICI.NS", "SBILIFE.NS",
    "HDFCLIFE.NS", "ICICIPRULI.NS", "PFC.NS", "REC.NS", "JIOFIN.NS", "PAYTM.NS",

    # --- IT & TECH ---
    "INFY.NS", "HCLTECH.NS", "WIPRO.NS", "TECHM.NS", "LTIM.NS", "OFSS.NS",
    "PERSISTENT.NS", "KPITTECH.NS", "COFORGE.NS", "MPHASIS.NS", "ZOMATO.NS",
    "NAUKRI.NS", "PBFINTECH.NS", "AFFLE.NS", "HAPPSTMNDS.NS", "CDSL.NS",

    # --- AUTO & EV ---
    "MARUTI.NS", "M&M.NS", "HEROMOTOCO.NS", "BAJAJ-AUTO.NS", "EICHERMOT.NS",
    "TVSMOTOR.NS", "ASHOKLEY.NS", "BHARATFORG.NS", "MOTHERSON.NS", "MRF.NS",
    "BOSCHLTD.NS", "EXIDEIND.NS", "AMARAJABAT.NS",

    # --- ENERGY, POWER & INFRA ---
    "RELIANCE.NS", "ONGC.NS", "NTPC.NS", "POWERGRID.NS", "BPCL.NS", "IOC.NS",
    "COALINDIA.NS", "GAIL.NS", "HPCL.NS", "IGL.NS", "MGL.NS", "LT.NS",
    "HAL.NS", "BEL.NS", "BHEL.NS", "MAZDOCK.NS", "COCHINSHIP.NS", "IRFC.NS",
    "RVNL.NS", "IRCTC.NS", "CONCOR.NS", "RAILTEL.NS", "SJVN.NS", "NHPC.NS",

    # --- CONSUMER, PHARMA & OTHERS ---
    "HINDUNILVR.NS", "ITC.NS", "ASIANPAINT.NS", "NESTLEIND.NS", "BRITANNIA.NS",
    "HAVELLS.NS", "DABUR.NS", "GODREJCP.NS", "MARICO.NS",
    "SUNPHARMA.NS", "CIPLA.NS", "DRREDDY.NS", "DIVISLAB.NS", "APOLLOHOSP.NS",
    "LUPIN.NS", "ALKEM.NS", "AUROPHARMA.NS", "BIOCON.NS", "LAURUSLABS.NS",
    "ULTRACEMCO.NS", "GRASIM.NS", "JSWSTEEL.NS", "HINDALCO.NS", "JINDALSTEL.NS",
    "SAIL.NS", "VEDL.NS", "NMDC.NS", "PIIND.NS", "UPL.NS", "SRF.NS", "PIDILITIND.NS"
]

# ==============================================================================
# 🛠 LOGGING & SETUP
# ==============================================================================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==============================================================================
# 📟 HELPER FUNCTIONS
# ==============================================================================

def get_paginated_keyboard(stocks, page=0, prefix="stock_"):
    total_stocks = len(stocks)
    start_index = page * STOCKS_PER_PAGE
    end_index = start_index + STOCKS_PER_PAGE
    current_page_stocks = stocks[start_index:end_index]

    keyboard = []
    row = []
    for stock in current_page_stocks:
        clean_name = stock.replace(".NS", "")
        row.append(InlineKeyboardButton(clean_name, callback_data=f"{prefix}{stock}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"page_{page-1}"))
    if end_index < total_stocks:
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"page_{page+1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)

    keyboard.append([InlineKeyboardButton("🔍 Search Stock", callback_data="cmd_search")])
    keyboard.append([InlineKeyboardButton("💼 My Portfolio", callback_data="cmd_portfolio")])
    return InlineKeyboardMarkup(keyboard)

def generate_stock_graph(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="6mo")
        if hist.empty: return None

        plt.figure(figsize=(10, 5))
        plt.plot(hist.index, hist['Close'], label='Close Price', color='blue')
        plt.title(f"{symbol} - Last 6 Months")
        plt.xlabel("Date")
        plt.ylabel("Price (INR)")
        plt.grid(True)
        plt.legend()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        return buf
    except Exception as e:
        print(f"❌ Graph Error: {e}")
        return None

def algo_trading_signal(hist):
    if len(hist) < 50: return "⚪ NO DATA", 0, 0
    hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
    hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
    
    sma_20 = hist['SMA_20'].iloc[-1]
    sma_50 = hist['SMA_50'].iloc[-1]

    signal = "HOLD 🟡"
    if sma_20 > sma_50: signal = "BUY 🟢"
    elif sma_20 < sma_50: signal = "SELL 🔴"
    
    return signal, sma_20, sma_50

async def fetch_stock_analysis(symbol):
    try:
        print(f"📡 Fetching data for: {symbol}")
        stock = yf.Ticker(symbol)
        info = stock.info
        hist = stock.history(period="3mo")
        
        if hist.empty: return None, None

        current_price = info.get("currentPrice")
        if current_price is None: current_price = hist["Close"].iloc[-1]

        market_cap = info.get("marketCap", "N/A")
        pe_ratio = info.get("trailingPE", "N/A")
        
        algo_signal, sma20, sma50 = algo_trading_signal(hist)

        msg = (
            f"📈 *{symbol} Analysis*\n\n"
            f"💰 *Price:* ₹{current_price:,.2f}\n"
            f"🤖 *Algo Signal:* {algo_signal}\n"
            f"📊 *Indicators:* SMA20 ({sma20:.1f}) | SMA50 ({sma50:.1f})\n"
            f"📉 *P/E Ratio:* {pe_ratio}\n"
        )
        return msg, current_price
    except Exception as e:
        print(f"❌ ERROR fetching {symbol}: {e}")
        return None, None

# ==============================================================================
# 💰 PAPER TRADING ENGINE
# ==============================================================================
def init_portfolio(context):
    if "portfolio" not in context.user_data:
        context.user_data["portfolio"] = {
            "cash": INITIAL_CAPITAL,
            "holdings": {}  # Format: {"TATA.NS": {"qty": 10, "avg_price": 500}}
        }

def execute_trade(context, symbol, action, price, qty=10):
    init_portfolio(context)
    pf = context.user_data["portfolio"]
    total_cost = price * qty

    if action == "BUY":
        if pf["cash"] >= total_cost:
            pf["cash"] -= total_cost
            if symbol in pf["holdings"]:
                # Averaging
                old_qty = pf["holdings"][symbol]["qty"]
                old_avg = pf["holdings"][symbol]["avg_price"]
                new_avg = ((old_qty * old_avg) + total_cost) / (old_qty + qty)
                pf["holdings"][symbol]["qty"] += qty
                pf["holdings"][symbol]["avg_price"] = new_avg
            else:
                pf["holdings"][symbol] = {"qty": qty, "avg_price": price}
            return True, f"✅ Bought {qty} of {symbol} at ₹{price:.2f}"
        else:
            return False, "❌ Insufficient Funds!"

    elif action == "SELL":
        if symbol in pf["holdings"] and pf["holdings"][symbol]["qty"] >= qty:
            pf["holdings"][symbol]["qty"] -= qty
            pf["cash"] += total_cost
            # Remove if 0
            if pf["holdings"][symbol]["qty"] == 0:
                del pf["holdings"][symbol]
            return True, f"✅ Sold {qty} of {symbol} at ₹{price:.2f}"
        else:
            return False, "❌ Insufficient Holdings!"

# ==============================================================================
# 🤖 BOT HANDLERS
# ==============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init_portfolio(context)
    context.user_data["searching"] = False
    context.user_data["current_list"] = STOCK_LIST
    
    cash = context.user_data["portfolio"]["cash"]
    await update.message.reply_text(
        f"🤖 *Algo Trading Bot Active*\n"
        f"💰 *Virtual Balance:* ₹{cash:,.2f}\n\n"
        f"Select a stock to Analyze & Trade:",
        reply_markup=get_paginated_keyboard(STOCK_LIST, page=0),
        parse_mode="Markdown"
    )

async def portfolio_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init_portfolio(context)
    pf = context.user_data["portfolio"]
    
    msg = f"💼 *Your Portfolio*\n\n💰 *Cash:* ₹{pf['cash']:,.2f}\n\n*Holdings:*\n"
    
    if not pf["holdings"]:
        msg += "_(No active trades)_"
    else:
        for symbol, data in pf["holdings"].items():
            msg += f"• *{symbol}*: {data['qty']} Qty (Avg: ₹{data['avg_price']:.1f})\n"

    keyboard = [[InlineKeyboardButton("🔙 Back to Market", callback_data="cmd_back")]]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    else:
        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # --- NAVIGATION ---
    if data.startswith("page_"):
        page_num = int(data.split("_")[1])
        current_list = context.user_data.get("current_list", STOCK_LIST)
        await query.edit_message_reply_markup(reply_markup=get_paginated_keyboard(current_list, page=page_num))

    elif data == "cmd_search":
        context.user_data["searching"] = True
        await query.edit_message_text("🔍 *Type stock name (e.g., TATA, ADANI)*", parse_mode="Markdown")
    
    elif data == "cmd_portfolio":
        await portfolio_handler(update, context)

    elif data == "cmd_back":
        context.user_data["searching"] = False
        context.user_data["current_list"] = STOCK_LIST
        await query.edit_message_text(
            "📈 *Market Dashboard*",
            reply_markup=get_paginated_keyboard(STOCK_LIST, page=0),
            parse_mode="Markdown"
        )

    # --- STOCK ANALYSIS ---
    elif data.startswith("stock_"):
        stock_symbol = data.replace("stock_", "")
        await query.edit_message_text(f"⏳ *Analyzing {stock_symbol}...*", parse_mode="Markdown")
        
        text_report, price = await fetch_stock_analysis(stock_symbol)
        
        if text_report:
            # SAVE PRICE TO CONTEXT FOR TRADING
            context.user_data["last_price"] = price
            context.user_data["last_symbol"] = stock_symbol

            keyboard = [
                [
                    InlineKeyboardButton(f"Buy 10 (@{price:.0f})", callback_data=f"buy_{stock_symbol}"),
                    InlineKeyboardButton(f"Sell 10 (@{price:.0f})", callback_data=f"sell_{stock_symbol}")
                ],
                [InlineKeyboardButton("📊 View Graph", callback_data=f"graph_{stock_symbol}")],
                [InlineKeyboardButton("🔙 Back", callback_data="cmd_back")]
            ]
            await query.edit_message_text(text_report, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        else:
            await query.edit_message_text(f"❌ Error fetching {stock_symbol}.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="cmd_back")]]))

    # --- GRAPH ---
    elif data.startswith("graph_"):
        stock_symbol = data.replace("graph_", "")
        await query.message.reply_text(f"📉 *Generating Graph...*", parse_mode="Markdown")
        img = generate_stock_graph(stock_symbol)
        if img: await query.message.reply_photo(photo=img)

    # --- TRADING EXECUTION ---
    elif data.startswith("buy_") or data.startswith("sell_"):
        action, symbol = data.split("_")
        action = action.upper()
        
        # Use stored price or fetch fresh if needed (using stored for speed here)
        price = context.user_data.get("last_price", 0)
        
        success, msg = execute_trade(context, symbol, action, price, qty=10)
        
        # Refresh Portfolio View
        pf = context.user_data["portfolio"]
        updated_msg = f"{msg}\n\n💰 *New Balance:* ₹{pf['cash']:,.2f}"
        
        keyboard = [[InlineKeyboardButton("💼 View Portfolio", callback_data="cmd_portfolio"), InlineKeyboardButton("🔙 Market", callback_data="cmd_back")]]
        await query.edit_message_text(updated_msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("searching"): return

    query_text = update.message.text.upper().strip()
    matches = [s for s in STOCK_LIST if query_text in s]
    
    if not matches:
        await update.message.reply_text(f"❌ No matches for '{query_text}'", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="cmd_back")]]))
        return

    context.user_data["current_list"] = matches
    await update.message.reply_text(f"✅ Found {len(matches)} matches:", reply_markup=get_paginated_keyboard(matches, page=0))

# ==============================================================================
# 🚀 MAIN
# ==============================================================================
def main():
    print("🚀 Starting Trading Bot...")
    if TELEGRAM_BOT_TOKEN == "PASTE_YOUR_NEW_TOKEN_HERE":
        print("❌ ERROR: Update the TOKEN!")
        return

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("portfolio", portfolio_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("✅ Bot is polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
