import asyncio
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN
from user_watchlist import get_all_users
from openclaw_agent import handle_stock_query

# Initialize Telegram bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def run_daily_alerts():
    """
    Sends daily stock summary to all users
    at scheduled time (Railway Cron).
    """
    users = get_all_users()

    if not users:
        print("⚠️ No users found in watchlist")
        return

    for chat_id, stocks in users.items():
        if not stocks:
            continue

        message = "📊 *Daily Stock Market Summary*\n\n"

        for stock in stocks:
            try:
                analysis = handle_stock_query(stock)
                message += f"{analysis}\n\n"
            except Exception as e:
                print(f"❌ Error processing {stock}: {e}")

        try:
            await bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode="Markdown"
            )
            print(f"✅ Sent daily alert to {chat_id}")
        except Exception as e:
            print(f"❌ Failed to send message to {chat_id}: {e}")

if __name__ == "__main__":
    asyncio.run(run_daily_alerts())
