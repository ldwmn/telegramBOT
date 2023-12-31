from telegram.ext import Updater, Dispatcher, CallbackContext
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler
from telegram.ext import Filters
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
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
    set_timer_handler = CommandHandler('set', set_timer)
    echo_handler = MessageHandler(Filters.text, do_echo)
    start_handler = CommandHandler(['start', 'help'], do_start)
    keyboard_handler = CommandHandler('keyboard', do_keyboard)
    inline_keyboard_handler = CommandHandler('inline_keyboard', do_inline_keyboard)
    callback_handler = CallbackQueryHandler(keyboard_react)


    dispatcher.add_handler(set_timer_handler)
    dispatcher.add_handler(keyboard_handler)
    dispatcher.add_handler(inline_keyboard_handler)
    dispatcher.add_handler(callback_handler)
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

    text = [
        f'Привет, <b>{user_full_name}!</b>',
        'Этот бот знает команды, например:',
        '/start - <i>перезапустит бота</i> ',
        '/help - <i>поможет тебе, если у тебя что-то не получается</i>',
        '/keyboard - <i>вызовет клавиатуру </i>',
        '/inline_keyboard - <i>тоже вызовет клавиатуру </i>',
        '/set - <i>cсек </i> '
        f'<code>secret</code>',
        '<a href = "https://github.com/ldwmn/telegramBOT/blob/main/TelegramBotPy.py"> Сайтик </a>'

    ]
    text = '\n'.join(text)


    '''
    html 
    < b > Сам жирный < / b >
    < i > Курсив < / i >
    < code > код < / code >
    < s > перечеркнутый < / s >
    < u > подчеркнутый < / u >
    < pre
    language = "c++" > код </pre>
    <a href = "smth.ru" > Сайт </a>
    '''
    update.message.reply_text(text, parse_mode=ParseMode.HTML)

    #logger.info(f'{username=} {user_id=} вызвал функцию do_start, написал: {text}')


def do_keyboard(update=Update, context=CallbackContext):
    buttons = [
        ['/help', '/start'],
        ['c', 'd'],
        ['e', 'f']
    ]

    text = 'выбери из списка'
    keyboard = ReplyKeyboardMarkup(buttons)
    update.message.reply_text(
        text,
        reply_markup=keyboard
    )


def do_inline_keyboard(update=Update, context=CallbackContext):
    user_id = update.message.from_user.id
    logger.info(f'{user_id=} вызвал функцию do_inline_keyboard')

    buttons = [
        ['/help', '/start'],
        ['c', 'd'],
        ['e', 'f']
    ]
    keyboard_buttons = [[InlineKeyboardButton(text=text, callback_data=text) for text in row] for row in buttons]

    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    text = 'выбери:'
    update.message.reply_text(
        text,
        reply_markup=keyboard
    )


def keyboard_react(update=Update, context=CallbackContext):
    '''query = update.callback_query

    text = 'Выбери еще раз' #написать ответ для inline_keyboard
    update.message.reply_text(
        text
    )'''
    pass

def set_timer(update=Update, context=CallbackContext):
    context.job_queue.run_repeating(show_seconds, 10)

def show_seconds(context=CallbackContext):
    user_id = 6652575831
    context.bot.send_message(user_id, 'прошло 10 секунд')
    pass



if __name__ == '__main__':
    main()