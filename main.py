import os
import asyncio
import csv
from telegram import Update, InputFile, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# -------------------------
# BOT TOKEN
# -------------------------
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing!")

# -------------------------
# Load valid numbers from CSV
# -------------------------
def load_valid_numbers(file_path="valid_numbers.csv"):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

VALID_NUMBERS = load_valid_numbers()

# -------------------------
# Global flags and tracking
# -------------------------
BOT_ACTIVE = True
USER_PENDING_AUTH = {}  # track which user is waiting to share number

# -------------------------
# Command handlers
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive 🚀")

# Stop bot (admin only optional)
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BOT_ACTIVE
    BOT_ACTIVE = False
    await update.message.reply_text("Bot is now stopped ⛔")

# Resume bot
async def resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BOT_ACTIVE
    BOT_ACTIVE = True
    await update.message.reply_text("Bot resumed ✅")

# /get command → request phone number
async def get_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not BOT_ACTIVE:
        return

    user_id = update.message.from_user.id

    # Ask user to share phone number
    button = KeyboardButton("Share Phone Number", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)

    USER_PENDING_AUTH[user_id] = True  # mark user as pending auth
    await update.message.reply_text(
        "Please share your mobile number to access the document:",
        reply_markup=reply_markup
    )

# Handle phone number shared by user
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not BOT_ACTIVE:
        return

    user_id = update.message.from_user.id

    if USER_PENDING_AUTH.get(user_id):
        contact = update.message.contact
        phone = contact.phone_number

        # Normalize phone numbers if needed
        if phone.startswith("0"):
            phone = "+91" + phone[1:]  # example for India

        if phone in VALID_NUMBERS:
            file_path = "sample.pdf"
            if os.path.exists(file_path):
                await update.message.reply_document(document=InputFile(file_path))
            else:
                await update.message.reply_text("PDF not found ❌")
        else:
            await update.message.reply_text("Your number is not authorized ❌")

        # Remove from pending
        USER_PENDING_AUTH.pop(user_id, None)

# -------------------------
# Build the bot application
# -------------------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(CommandHandler("resume", resume))
app.add_handler(CommandHandler("get", get_pdf))
app.add_handler(MessageHandler(filters.CONTACT, handle_contact))

# -------------------------
# Run bot
# -------------------------
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(app.run_polling())
