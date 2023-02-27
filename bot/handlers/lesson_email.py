from create_bot import bot
from services.service_common import check_user_exist_or_create
from data.data_for_lessons import data_dct, active_users
import time
from aiogram import Dispatcher, types
from services.service_common import send_message_as_a_voice


async def lesson_email(message):
    print(message.from_user.id)
    await check_user_exist_or_create(message.from_user.id)
    
    # 1 message
    await bot.send_message(message.chat.id, data_dct['email_messages']['message_1'], parse_mode='html')
    # 2 message
    await bot.send_message(message.chat.id, data_dct['email_messages']['message_2'], parse_mode='html')
    # голосовое ЭТ
    active_users[message.from_user.id]['Dialog'] = active_users[message.from_user.id]['Dialog'] + '\n' + 'Alice: ' + data_dct['email_messages']['message_3']
    
    await send_message_as_a_voice(message, data_dct['email_messages']['message_3'], 'facebook')

    # говорим ученику повторить ЭТ
    await bot.send_message(message.chat.id, data_dct['email_messages']['message_4'], parse_mode='html')
    active_users[message.from_user.id]['State'] = 'at_0_at'


def register_handlers_lesson_time(dp : Dispatcher):
    # dp.register_message_handler(send_to_admin_launch)
    dp.register_message_handler(lesson_email, commands=['email'])