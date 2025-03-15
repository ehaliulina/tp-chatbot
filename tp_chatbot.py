from telegram import Update 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext 
import openai 

# Set up API keys
TELEGRAM_BOT_TOKEN = "your_telegram_api_token_here"
OPENAI_API_KEY = "your_openai_api_key_here"

openai.api_key = OPENAI_API_KEY 

def handle_message(update: Update, context: CallbackContext): 
    user_message = update.message.text 
    response = openai.ChatCompletion.create( 
        model="gpt-4", 
        messages=[{"role": "system", "content": "You are a transfer pricing expert answering questions concisely."},
         {"role": "user", "content": user_message}] 
         )
          reply = response["choices"][0]["message"]["content"] 
          update.message.reply_text(reply) 
          
          def main():
             updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True) 
             dp = updater.dispatcher 
             dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message)) 
             updater.start_polling() 
             updater.idle() 
             if name == "main": 
                main()