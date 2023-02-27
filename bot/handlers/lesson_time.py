from create_bot import bot
import requests
from services.service_common import check_user_exist_or_create
from data.data_for_lessons import data_dct, active_users
import time
from aiogram import Dispatcher, types
from services.service_common import send_message_as_a_voice



async def lesson_time(message: types.Message):
    image_url = 'https://oneminuteenglish.org/wp-content/uploads/2020/05/ten-past-1.png'
    response = requests.get(image_url)
    image = response.content
    
    print(message.from_user.id)
    await check_user_exist_or_create(message.from_user.id)
    
    # 1 message
    await bot.send_message(message.chat.id, data_dct['time_messages']['part_1'], parse_mode='html')
    # 1.1 message 
    await bot.send_photo(message.chat.id, image, parse_mode='html')
    # 2 message
    await bot.send_message(message.chat.id, data_dct['time_messages']['part_2'], parse_mode='html')
    # 2.2 message 
    await bot.send_message(message.chat.id, data_dct['time_messages']['part_yt_1'], parse_mode='html')
    # 2.2 message
    await bot.send_message(message.chat.id, data_dct['time_messages']['part_yt_2'], parse_mode='html')
    
    time.sleep(2)
    
    # 3 message
    await bot.send_message(message.chat.id, data_dct['time_messages']['part_3'], parse_mode='html')
    # 4 message
    await bot.send_message(message.chat.id, data_dct['time_messages']['practice_mes_1'], parse_mode='html')    
    # voice
    active_users[message.from_user.id]['Dialog'] = active_users[message.from_user.id]['Dialog'] + '\n' + 'Alice: ' + \
    data_dct['time_messages']['voice_mess_1']
    await send_message_as_a_voice(message, data_dct['time_messages']['voice_mess_1'], 'facebook')
    # message 6 экшн
    await bot.send_message(message.chat.id, data_dct['time_messages']['part_6'], parse_mode='html')
    
    active_users[message.from_user.id]['State'] = 'time_0'
    
    ## i something send and message should be in a db?


def register_handlers_lesson_time(dp : Dispatcher):
    # dp.register_message_handler(send_to_admin_launch)
    dp.register_message_handler(lesson_time, commands=['time'])