import telebot
from flask import Flask
import threading

TOKEN = "your_telegram_bot_token"
bot = telebot.TeleBot(TOKEN)

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
    
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
import openai
import asyncio

# Set up API keys
TELEGRAM_BOT_TOKEN = "7749529825:AAGePLg3YOrDYTJ0vk59QVprNf_jMScRuyE"
OPENAI_API_KEY = "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"

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
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
