import Token as key
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import *
from Respons import *

PENILAIAN = range(1)
R = Respons()

class Chatbot():
    def start_command(update, context):
        update.message.reply_text('Silahkan tanyakan sesuatu yang berkaitan dengan pertanyaan akademik jurusan teknik informatika fakultas ilmu komputer universitas sriwijaya!\n\nSeperti:\n"Apa syarat kerja praktik ?"\n"Bagaiamana cara daftar skripsi ?"\n"Cara mengurus KHS yang hilang"')

    def handle_message(update, context):
        text = str(update.message.text)
        respons = R.chatbotResponse(text)
        if respons == True:
            update.message.reply_text('Pertanyaan tidak dapat dimengerti atau tidak tersedia')
            return ConversationHandler.END
        update.message.reply_text(respons[0])
        context.user_data['pertanyaan'] = text
        context.user_data['data_log'] = respons[1]
        reply_keyboard = [['Sesuai', 'Tidak Sesuai']]
        update.message.reply_text(
            'Apakah jawaban yang diberikan sudah sesuai ?',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Sesuai atau Tidak Sesuai?'
            ),
        )
        return PENILAIAN

    def penilaian (update, context) -> int:
        kesimpulan = str(update.message.text)
        pertanyaan = context.user_data['pertanyaan']
        log = context.user_data['data_log']
        R.simpan_penilaian(pertanyaan,log,kesimpulan)
        
        # update.message.reply_text('Terima kasih atas penilaiannya')
        update.message.reply_text(
            'Terima kasih atas penilaiannya', reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    def cancel(update: Update, context: CallbackContext) -> int:
        user = update.message.from_user
        update.message.reply_text(
            'Silahkan tanyakan pertanyaan yang lain', reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    def error(update, context):
        print(f"Update {update} caused error {context.error}")

    def main(self):
        updater = Updater(key.API_KEYS)
        dp = updater.dispatcher
       
        # dp.add_handler(MessageHandler(Filters.text, handle_message))
        conv_handler = ConversationHandler(
            entry_points=[MessageHandler(Filters.text, Chatbot.handle_message)],
            states={
                PENILAIAN: [MessageHandler(Filters.regex('^(Sesuai|Tidak Sesuai)$'), Chatbot.penilaian)],
            },
            fallbacks=[CommandHandler('cancel', Chatbot.cancel)],
        )
        dp.add_handler(CommandHandler("start", Chatbot.start_command))
        dp.add_handler(conv_handler)
        # dp.add_error_handler(error)
        
        updater.start_polling()
        updater.idle()

print ("Bot start...")

Run = Chatbot()

if __name__ == '__main__':
    Run.main()