from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import os
TOKEN = os.getenv("TOKEN")

# TOKEN = "6591994405:AAFSYBd9f-td2kIHxb583_oGqMEBSqv1rww"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am running on JustRunMy.App 🚀")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
