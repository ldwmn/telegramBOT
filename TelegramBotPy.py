from telegram.ext import Updater, Dispatcher, CallbackContext
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler
from telegram.ext import Filters
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import telegramTOKEN
import logging
import datetime

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
    inline_keyboard_handler = CommandHandler('inline_keyboard', do_inline_keyboard)
    set_timer_handler = CommandHandler('set', set_timer)
    callback_handler = CallbackQueryHandler(keyboard_react)
    stop_timer_handler = CommandHandler('stop', delete_timer)


    dispatcher.add_handler(keyboard_handler)
    dispatcher.add_handler(inline_keyboard_handler)
    dispatcher.add_handler(callback_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(set_timer_handler)
    dispatcher.add_handler(stop_timer_handler)

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
        '/set - <i>cсек </i> ',
        '/stop - <i>останвка таймера</i> '
        f'<code>secret</code>',
        '<a href = "https://github.com/ldwmn/telegramBOT/blob/main/TelegramBotPy.py">Сайтик</a>'

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

def do_inline_keyboard(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    logger.info(f'{user_id=} вызвал функцию do_inline_keyboard')
    buttons = [
        ['Раз', 'Два'],
        ['Три', 'Четыре'],
        ['Погода в Москве']
    ]
    keyboard_buttons = [[InlineKeyboardButton(text=text, callback_data=text) for text in row] for row in buttons]
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    logger.info(f'Создана клавиатура {keyboard}')
    text = 'Выбери одну из опций на клавиатуре'
    update.message.reply_text(
        text,
        reply_markup=keyboard
    )
    logger.info(f'Ответ улетел')

def keyboard_react(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = update.effective_user.id
    logger.info(f'{user_id=} вызвал функцию keyboard_react')
    buttons = [
        ['Раз', 'Два'],
        ['Три', 'Четыре'],
        ['Погода в Москве']
    ]
    for row in buttons:
        if query.data in row:
            row.pop(row.index(query.data))
    keyboard_buttons = [[InlineKeyboardButton(text=text, callback_data=text) for text in row] for row in buttons]
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    text = 'Выбери другую опцию на клавиатуре'
    query.edit_message_text(
        text,
        reply_markup=keyboard
    )

def set_timer(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    context.bot_data['user_id'] = user_id
    context.bot_data['timer'] = datetime.datetime.now()
    context.bot_data['job_id'] = context.job_queue.run_repeating(show_seconds, 1)

def show_seconds(context: CallbackContext):
    logger.info(f'{context.job_queue.jobs()}')

    user_id = context.bot_data['user_id']
    timer = datetime.datetime.now() - context.bot_data['timer']
    timer = timer.seconds
    context.bot_data['timer'] = timer
    context.bot.send_message(user_id, f'прошло {timer} секунд')



def delete_timer(update: Update, context: CallbackContext):
    logger.info(f'Запущена функция  delete_timer')
    context.bot_data['job_id'].shedule_removal
    for job in context.job_queue.jobs():
        job.schedule_removal()

    update.message.reply_text(f'Таймер остановлен.')


if __name__ == '__main__':
    main()