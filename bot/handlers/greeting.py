from aiogram import Dispatcher, types
from create_bot import bot
from config import admin_id
from services.service_common import check_user_exist_or_create
from data import data_for_lessons
from keyboards.client_kb import kb_client, kb_client_lessons
import create_bot


""" Function for sending the message to admin that bot started """
async def send_to_admin_launch(dp):
    await bot.send_message(chat_id=admin_id, text='Bot started')


async def welcome(message: types.Message):
    print(message.from_user.id)
    
    await check_user_exist_or_create(message.from_user.id)
    
    # data_for_lessons.data_dct['welcome'].format(message.from_user, await bot.get_me())
    await bot.send_message(message.chat.id, data_for_lessons.data_dct['greeting'].format(message.from_user, await bot.get_me()), parse_mode='html', \
                            reply_markup=kb_client)


async def send_lessons(message: types.Message):
    create_bot.TYPE_OF_ACTIVITY = 'Lessons'
    
    await check_user_exist_or_create(message.from_user.id)
    await message.answer('Lessons below!', reply_markup=kb_client_lessons)


def register_handlers_client(dp : Dispatcher):
    # dp.register_message_handler(send_to_admin_launch)
    dp.register_message_handler(welcome, commands=['start'])
    dp.register_message_handler(send_lessons, commands=['Lessons'])