import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Read token from environment
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing! Set it in Render Environment.")

# -------------------------
# Command Handlers
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! SAIL-CMO Welcomes you!! ")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "I am your Telegram bot for downloading your documents \n\n"
        "/start - Start the bot\n"
        "/help - Show this message\n"
        "/ping - Check if bot is alive"
    )
    await update.message.reply_text(help_text)

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong! 🏓 I'm running.")

# -------------------------
# Build the application
# -------------------------
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("ping", ping))

# -------------------------
# Run the bot (Render-compatible)
# -------------------------
if __name__ == "__main__":
    # Manually create an event loop in the main thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(app.run_polling())
