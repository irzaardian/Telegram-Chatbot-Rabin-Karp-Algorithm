import Token as key
from telegram.ext import *
import Respons as R

def start_command(update, context):
    update.message.reply_text('Ketik sesuatu')

def handle_message(update, context):
    text = str(update.message.text)
    response = R.ChatbotResponse(text)
    update.message.reply_text(response)

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(key.API_KEYS)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
    
print ("Bot start...")

main()