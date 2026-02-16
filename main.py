from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 👉 PASTE YOUR BOT TOKEN BETWEEN QUOTES
TOKEN = "8466480154:AAFwBaOlbRYkRTLzPKxVjlC4COtT94_r_TE"


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is active and running!")


# /help command
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Available commands:\n/start\n/help")


def main():
    print("Bot starting...")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))

    print("Bot is polling...")
    app.run_polling()


if __name__ == "__main__":
    main()

