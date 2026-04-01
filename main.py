import os
import asyncio
import csv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# -------------------------
# BOT TOKEN
# -------------------------
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing!")

# -------------------------
# Load valid numbers
# -------------------------
def load_valid_numbers(file_path="valid_numbers.csv"):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

VALID_NUMBERS = load_valid_numbers()

# -------------------------
# Bot state
# -------------------------
BOT_ACTIVE = True
USER_PENDING_AUTH = {}  # user_id -> waiting for mobile

# -------------------------
# Command Handlers
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BOT_ACTIVE
    BOT_ACTIVE = True
    await update.message.reply_text(
        "Welcome Guest, This allow you to download your documents. Use /help to know more."
    )

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BOT_ACTIVE
    BOT_ACTIVE = False
    await update.message.reply_text(
        "Bye. This BOT stopped now. You can anytime start using /START command."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "/start - Start the bot\n"
        "/stop - Stop the bot\n"
        "/help - Show this help message\n"
        "/get - Get access to your document (mobile verification)"
    )
    await update.message.reply_text(help_text)

async def get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not BOT_ACTIVE:
        return
    user_id = update.message.from_user.id
    USER_PENDING_AUTH[user_id] = True

    # Ask user to share mobile number
    button = KeyboardButton("Share Mobile Number", request_contact=True)
    markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "Please share your mobile number to access the document.",
        reply_markup=markup
    )

# -------------------------
# Handle mobile number
# -------------------------
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not BOT_ACTIVE:
        return

    user_id = update.message.from_user.id
    if not USER_PENDING_AUTH.get(user_id):
        return

    contact = update.message.contact
    phone = contact.phone_number

    # Normalize if needed (example India)
    if phone.startswith("0"):
        phone = "+91" + phone[1:]

    if phone in VALID_NUMBERS:
        await update.message.reply_text("✅ Mobile number verified. Access granted.")
    else:
        await update.message.reply_text("❌ Mobile number not valid. Access denied.")

    # Remove pending state
    USER_PENDING_AUTH.pop(user_id, None)

# -------------------------
# Build bot application
# -------------------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("get", get))
app.add_handler(MessageHandler(filters.CONTACT, handle_contact))

# -------------------------
# Run bot
# -------------------------
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(app.run_polling())
