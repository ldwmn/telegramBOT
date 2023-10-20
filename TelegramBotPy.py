from telegram.ext import Updater, Dispatcher, CommandHandler
from telegram.ext import MessageHandler, CallbackContext
from telegram.ext import Filters
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import telegramTOKEN
import logging

TOKEN = telegramTOKEN.TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO
                    )
logger = logging.getLogger(__name__)

def main():
    updater = Updater(token=TOKEN)
    dispatcher: Dispatcher = updater.dispatcher

    echo_handler = MessageHandler(Filters.text, do_echo)
    start_handler = CommandHandler(['start', 'help'], do_start)
    keyboard_handler = CommandHandler('keyboard', do_keyboard)

    dispatcher.add_handler(keyboard_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    logger.info(updater.bot.getMe())
    updater.idle()

def do_echo(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    text = update.message.text

    logger.info(f'{username=} {user_id=} вызвал функцию echo, написал:  {text}')
    answer = [f'Твой {user_id=},',
              f'Твой {username=},',
              f'Ты написал {text}'
    ]

    answer = '\n'.join(answer)
    update.message.reply_text(answer)

def do_start(update=Update, context=CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    user_full_name = update.message.from_user.full_name
    text = [f'Привет, {user_full_name}',
            'Я знаю комманды:',
            '/start',
            '/help',
            '/keyboard'
    ]
    text = '\n'.join(text)


    update.message.reply_text(text)

    #logger.info(f'{username=} {user_id=} вызвал функцию do_start, написал: {text}')


def do_keyboard(update=Update, context=CallbackContext):
    buttons = [
        ['a', 'b'],
        ['c', 'd'],
        ['e', 'f']
    ]

    text = 'выбери из списка'
    keyboard = ReplyKeyboardMarkup(buttons)
    update.message.reply_text(
        text,
        reply_markup=keyboard
    )

if __name__ == '__main__':
    main()