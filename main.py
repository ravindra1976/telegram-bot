import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ✅ Read the bot token from environment
TOKEN = os.getenv("BOT_TOKEN")  # Make sure the env variable name matches exactly

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing! Please set it in Render.")

# ✅ Command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive 🚀")

# ✅ Build the application
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

# ✅ Async main function
async def main():
    await app.run_polling()

# ✅ Run the bot safely
if __name__ == "__main__":
    asyncio.run(main())
