from telegram import Update 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext 
import openai 

# Set up API keys
TELEGRAM_BOT_TOKEN = "7749529825:AAGePLg3YOrDYTJ0vk59QVprNf_jMScRuyE"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY 

def handle_message(update: Update, context: CallbackContext): 
    user_message = update.message.text 
    response = openai.ChatCompletion.create( 
        model="gpt-4", 
        messages=[
            {"role": "system", "content": "You are a transfer pricing expert answering questions concisely."},
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
