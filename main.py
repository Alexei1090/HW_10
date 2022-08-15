from asyncio import Task
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
import os
from config import TOKEN


TASK = 0
w = 'чаты'




def start_play(token):
    bot = Bot(token)
    updater = Updater(token)
    dispatcher = updater.dispatcher
    print('Бот работает...')

    def start(update, context):
        context.bot.send_message(update.effective_chat.id, "Привет. Игра  'Быки и коровы' началась. Нужно угадать слово из 4 букв")
        return TASK


    def play(update, context):
        b = 0
        c = 0
        w_new = update.message.text
        if len(w_new) == 4:
            for i,j in zip(w,w_new):
                if j in w:
                    if i == j:
                        b += 1
                    else:
                        c += 1
            context.bot.send_message(update.effective_chat.id, f'Быков {b}, Коров {c}')
            if b == 4:
                context.bot.send_message(update.effective_chat.id, 'Браво, Вы победили!')
                return ConversationHandler.END
            else:
                context.bot.send_message(update.effective_chat.id, 'Вы не угадали слово, введите другое слово')
                return TASK
        else:
            context.bot.send_message(update.effective_chat.id, 'Вы ввели слово не из 4 букв')
            return TASK


   

    def stop(update, context):
        context.bot.send_message(update.effective_chat.id, "Хорошего дня!")



    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, start)],
        states={
            TASK: [MessageHandler(Filters.text, play)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    stop_handler = CommandHandler('stop', stop)


    dispatcher.add_handler(stop_handler)
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


def main():
    start_play(TOKEN)
    print('Бот остановлен!')


if __name__ == "__main__":
    main()
