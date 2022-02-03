import Token as key
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import *
import Respons as R

PENILAIAN = range(1)

def start_command(update, context):
    update.message.reply_text('Ketik sesuatu')

def handle_message(update, context):
    text = str(update.message.text)
    response = R.ChatbotResponse(text)
    update.message.reply_text(response)
    context.user_data['pertanyaan'] = text
    context.user_data['jawaban'] = response
    # penilaian(text, response)

    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [['Sesuai', 'Tidak Sesuai']]

    if response == "Pertanyaan tidak dapat dimengerti":
        return ConversationHandler.END
    else:
        update.message.reply_text(
            'Apakah jawaban yang diberikan sudah sesusai ?',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Sesuai atau Tidak Sesuai?'
            ),
        )
    # penilaian(text, response)
    return PENILAIAN

def penilaian (update, context) -> int:
    kesimpulan = str(update.message.text)
    # user_data = context.user_data
    pertanyaan = context.user_data['pertanyaan']
    jawaban = context.user_data['jawaban']
    R.simpan_penilaian(pertanyaan,jawaban,kesimpulan)
    
    update.message.reply_text('Terima kasih atas penilaiannya :)')
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    # logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(key.API_KEYS)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    # dp.add_handler(MessageHandler(Filters.text, handle_message))
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, handle_message)],
        states={
            PENILAIAN: [MessageHandler(Filters.regex('^(Sesuai|Tidak Sesuai)$'), penilaian)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dp.add_handler(conv_handler)

    dp.add_error_handler(error)
    
    updater.start_polling()
    updater.idle()
    
print ("Bot start...")

main()