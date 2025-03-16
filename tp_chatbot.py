import os
import telebot
from flask import Flask
import threading

# Load API keys from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate if tokens exist
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is missing! Check your environment variables.")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing! Check your environment variables.")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Initialize Flask app
app = Flask(name)

@app.route("/")
def home():
    return "Bot is running!"

def start_bot():
    """Function to start the Telegram bot."""
    bot.polling(non_stop=True)

if name == "main":
    # Start Telegram bot in a separate thread
    threading.Thread(target=start_bot).start()
    
    # Start Flask web server (Render requires an HTTP server)
    app.run(host="0.0.0.0", port=8080)

# --------------------- Telegram Bot with GPT-4 ---------------------

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
import openai
import asyncio

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a transfer pricing expert answering questions concisely."},
                {"role": "user", "content": user_message}
            ]
        )
        
        reply = response["choices"][0]["message"]["content"]
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("An error occurred. Please try again later.")
        print(f"Error: {e}")

def main():
    """Start the Telegram bot with GPT integration."""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if name == "main":
    main()
