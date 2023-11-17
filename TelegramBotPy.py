from telegram.ext import Updater, Dispatcher, CallbackContext
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler
from telegram.ext import Filters
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import telegramTOKEN
import logging
import datetime
from fsm import register_handler

TOKEN = telegramTOKEN.TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO
                    )
logger = logging.getLogger(__name__)

def main():
    updater = Updater(token=TOKEN)
    dispatcher: Dispatcher = updater.dispatcher
    echo_handler = MessageHandler(Filters.text, do_echo)
    start_handler = CommandHandler(['start'], do_start)
    keyboard_handler = CommandHandler('keyboard', do_keyboard)
    inline_keyboard_handler = CommandHandler('inline_keyboard', do_inline_keyboard)
    set_timer_handler = CommandHandler('set', set_timer)
    callback_handler = CallbackQueryHandler(keyboard_react)
    stop_timer_handler = CommandHandler('stop', delete_timer)
    help_handler = CommandHandler(['help'], do_help)


    dispatcher.add_handler(keyboard_handler)
    dispatcher.add_handler(inline_keyboard_handler)
    dispatcher.add_handler(callback_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(set_timer_handler)
    dispatcher.add_handler(stop_timer_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(register_handler)

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
        '<b>/register</b>  -    Зарегистрироваться'
        '<b>/start</b>  -  перезапустит бота',
        '<b>/help</b>  -  поможет тебе, если у тебя что-то не получается',
        '<b>/keyboard</b>  -  вызовет клавиатуру ',
        '<b>/inline_keyboard</b>  -  тоже вызовет клавиатуру ',
        '<b>/set</b>  -  Запустит секундомер ',
        '<b>/stop</b>  -    Остановит секундомер'

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


def do_help(update=Update, context=CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    user_full_name = update.message.from_user.full_name

    text = [
        f'Этот бот знает команды:',
        '<b>/start</b>  -  перезапустит бота',
        '<b>/help</b>  -  поможет тебе, если у тебя что-то не получается',
        '<b>/keyboard</b>  -  вызовет клавиатуру ',
        '<b>/inline_keyboard</b>  -  тоже вызовет клавиатуру ',
        '<b>/set</b>  -  Запустит секундомер ',
        '<b>/stop</b>  -    Остановит секундомер'

    ]
    text = '\n'.join(text)
    update.message.reply_text(text, parse_mode=ParseMode.HTML)

def do_keyboard(update=Update, context=CallbackContext):
    buttons = [
        ['/start', '/help'],
        ['/set', '/stop'],
        ['/inline_keyboard']
    ]

    text = 'Клавиатура включена '
    keyboard = ReplyKeyboardMarkup(buttons)
    update.message.reply_text(
        text,
        reply_markup=keyboard
    )
def do_inline_keyboard(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    logger.info(f'{user_id=} вызвал функцию do_inline_keyboard')
    buttons = [
        ['Секундомер', '/help'],
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
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    key = f'{user_id}_timer'

    logger.info(f'{user_id=} keyboard_react')
    print(query.data)
    if query.data == 'Секундомер':
        set_timer(update, context)
    if query.data == '/help':
        do_help(update, context)

    query.bot.send_message(
        chat_id=chat_id,
        reply_markup=ReplyKeyboardRemove()
    )

def set_timer(update, context):
    logger.info(f'Выполнена функция {set_timer}')
    user_id = update.effective_user.id
    context.bot_data["user_id"] = user_id
    context.bot_data["timer"] = datetime.datetime.now()
    context.bot_data['timer_job'] = context.job_queue.run_repeating(show_seconds, 1)

def show_seconds(context):
    global timer
    message_id = context.bot_data.get('message_id', None)
    user_id = context.bot_data["user_id"]
    timer = datetime.datetime.now() - context.bot_data['timer']
    timer = timer.seconds
    text = f'Прошло <b>{timer}</b> секунд, чтобы остановить нажми /stop'
    if not message_id:
        message = context.bot.send_message(user_id, text, parse_mode=ParseMode.HTML)
        context.bot_data['message_id'] = message.message_id
    else:
        context.bot.edit_message_text(text, chat_id=user_id, message_id=message_id, parse_mode=ParseMode.HTML)



def delete_timer(update: Update, context: CallbackContext):
    context.bot_data['timer_job'].schedule_removal()
    context.bot_data.clear()
    update.message.reply_text(f'Секундомер остановлен, прошло {timer} секунд')


if __name__ == '__main__':
    main()