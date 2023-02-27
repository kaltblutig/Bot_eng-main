from create_bot import bot
import create_bot
import requests
from services.service_common import check_user_exist_or_create
from data.data_for_lessons import data_dct, active_users
import time
import re
import random
from aiogram import Dispatcher, types
from services.service_voice_proc import get_student_voice_and_transcribe_wym, check_student_said_at, check_student_said_sky_correct, check_student_time_0, \
                                check_student_time_1, check_student_time_2, check_student_time_4, check_student_time_7, get_student_voice_and_transcribe
from services.service_common import send_message_as_a_voice
# нужно изменить этот флаг на prod, если вы собираетесь делать запрос на свой внутренний api 
from config import FLAG



# async def save_db(user_id, chat_id, username):
#     await save_to_db(
#         conversationId=str(chat_id) + "-angelina",
#         userId=user_id,
#         userName=username,
#         isStudent=1,
#         userSpeechRecordedAt=int(time.time()),
#         userSpeechRecordFormat='wav',
#         # userSpeech=Student_answer,
#         userSpeechRecordPath='last_voice_from_user' + str(user_id) + '.wav',
#         userSpeechRecordFileName='last_voice_from_user' + str(user_id) + '.wav',
#     )


async def voice_processing(message: types.Message):
    if create_bot.TYPE_OF_ACTIVITY == 'Lessons':
        print(message)
        user_id = message.from_user.id
        username = message.from_user.username
        chat_id = message.chat.id
        user_state = active_users[user_id]['State']
        print('State right now: ', user_state)
        
        await check_user_exist_or_create(user_id)


        if user_state == 'at_0_at':
            std_ans = await get_student_voice_and_transcribe_wym(message)
            comm_fr_gpt = await check_student_said_at(std_ans)
            print('Student answer: ', std_ans)
            print('Commentary from gpt: ', comm_fr_gpt)
            # await save_db(user_id, chat_id, username)
            
            await send_message_as_a_voice(message, comm_fr_gpt, 'murf')
            active_users[user_id]['State'] = 'at_1_sky'
            print(data_dct['voice_proccesing_messages']['at_0_at'])
            await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['at_0_at'], parse_mode='html')
            
        elif user_state == 'at_1_sky':
            std_ans = await get_student_voice_and_transcribe_wym(message)
            comm_fr_gpt = await check_student_said_sky_correct(std_ans)
            print('Student answer: ', std_ans)
            print('Commentary from gpt: ', comm_fr_gpt)
            # await save_db(user_id, chat_id, username)
            
            await send_message_as_a_voice(message, comm_fr_gpt, 'murf')

            if re.search(".+?@.+?(\.|dot).+?", std_ans.lower()):
                active_users[user_id]['State'] = 'at_3_text_email'
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['at_1_sky']['part_1'], parse_mode='html')
                await bot.send_message(message.chat.id, data_dct['voice_proccesing_messages']['at_1_sky']['part_2'], parse_mode='html')
            else:
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['at_1_sky']['part_3'], parse_mode='html')

        elif user_state == 'at_3_text_email':
            # ветка когда студент озвучивает емейл sky.gmail
            std_ans = await get_student_voice_and_transcribe_wym(message)
            comm_fr_gpt = await check_student_said_sky_correct(std_ans)
            print('Student answer: ', std_ans)
            print('Commentary from gpt: ', comm_fr_gpt)
            # await save_db(user_id, chat_id, username)

            await send_message_as_a_voice(message, comm_fr_gpt, 'murf')
            
            active_users[user_id]['Dialog'] = active_users[user_id]['Dialog'] + '\n' + 'Alice: ' + data_dct['voice_proccesing_messages']['at_3_text_email']['part_1']

            await send_message_as_a_voice(message, data_dct['voice_proccesing_messages']['at_3_text_email']['part_1'], 'murf')

        elif user_state == 'at_4_own_email_voice':
            # ветка когда студент озвучивает сам емейл
            std_ans = await get_student_voice_and_transcribe_wym(message)
            comm_fr_gpt = await check_student_said_sky_correct(std_ans)
            print('Student answer: ', std_ans)
            print('Commentary from gpt: ', comm_fr_gpt)
            # await save_db(user_id, chat_id, username)
            comm_fr_gpt_2 = await check_student_said_sky_correct(std_ans)

            await send_message_as_a_voice(message, comm_fr_gpt, 'murf')

            if re.search(".+?@.+?(\.|dot).+?", std_ans.lower()):
                active_users[user_id]['State'] = 'at_6_test'

                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['at_1_sky']['part_1'], parse_mode='html')
                await bot.send_message(chat_id, text=data_dct['voice_proccesing_messages']['at_4_own_email_voice']['part_3'], parse_mode='html')

                message_it = ' bootcamp@gmail.com'
                active_users[user_id]['Dialog'] = active_users[user_id]['Dialog'] + '\n' + 'Alice: ' + message_it
                
                await send_message_as_a_voice(message, message_it, 'murf')

                # Отправляем текст в Телеграм
                await bot.send_message(chat_id, text=data_dct['voice_proccesing_messages']['at_4_own_email_voice']['part_2'], parse_mode='html')

            else:
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['at_4_own_email_voice']['part_1'], parse_mode='html')

        elif user_state == 'time_0':
            # ветка когда студент озвучивает емейл sky.gmail
            std_ans = await get_student_voice_and_transcribe_wym(message)
            comm_fr_gpt = await check_student_time_0(std_ans)
            print('Student answer: ', std_ans)
            print('Commentary from gpt: ', comm_fr_gpt)
            # await save_db(user_id, chat_id, username)

            await send_message_as_a_voice(message, comm_fr_gpt, 'murf')

            if re.search(".+?(12|twelve).+?(o'clock|)+?", std_ans.lower()):

                active_users[user_id]['State'] = 'time_1'

                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['at_1_sky']['part_1'], parse_mode='html')
                active_users[user_id]['Question'] = data_dct['voice_proccesing_messages']['time_0']['part_1']
                await bot.send_message(chat_id, active_users[user_id]['Question'], parse_mode='html')

            else:
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_0']['part_2'], parse_mode='html')

        elif user_state == 'time_1':
            # ветка когда студент озвучивает емейл sky.gmail
            std_ans = await get_student_voice_and_transcribe(message)   # to do
            comm_fr_gpt = await check_student_time_1(std_ans)
            print('Student answer: ', std_ans)
            print('Commentary from gpt: ', comm_fr_gpt)
            # await save_db(user_id, chat_id, username)

            await send_message_as_a_voice(message, comm_fr_gpt, 'murf')

            # if re.search(".+?(it's|it).+?(5|five).+?(past).+?(12|twelve).+?", Student_answer.lower()):
            if re.search("(5|five).+?(past).+?", std_ans.lower()):

                active_users[user_id]['State'] = 'time_2'

                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_1']['part_1'], parse_mode='html')

                active_users[message.from_user.id]['Question'] = data_dct['voice_proccesing_messages']['time_1']['part_2']
                await bot.send_message(chat_id, active_users[user_id]['Question'], parse_mode='html')
            else:
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_0']['part_2'], parse_mode='html')

        elif user_state == 'time_2':
            # ветка когда студент озвучивает емейл sky.gmail
            std_ans = await get_student_voice_and_transcribe(message)   # to do
            comm_fr_gpt = await check_student_time_2(std_ans)
            print('Student answer: ', std_ans)
            print('Commentary from gpt: ', comm_fr_gpt)
            # await save_db(user_id, chat_id, username)

            await send_message_as_a_voice(message, comm_fr_gpt, 'murf')

            if re.search(".+?(it's )|(half )|(past )|.+?^|12|twelve|", std_ans.lower()):
                active_users[user_id]['State'] = 'time_3'
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_1']['part_1'], parse_mode='html')
                active_users[user_id]['Question'] = data_dct['voice_proccesing_messages']['time_2']['part_1']
                await bot.send_message(chat_id, active_users[user_id]['Question'], parse_mode='html')
            else:
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_0']['part_2'], parse_mode='html')

        elif user_state == 'time_3':
            # ветка когда студент озвучивает емейл sky.gmail
            std_ans = await get_student_voice_and_transcribe(message)   # to do
            comm_fr_gpt = await check_student_time_4(std_ans, active_users[user_id]['Question'])
            print('Student answer: ', std_ans)
            print('Commentary from gpt: ', comm_fr_gpt)
            # await save_db(user_id, chat_id, username)

            await send_message_as_a_voice(message, comm_fr_gpt, 'murf')

            if re.search("^it.+?|(29|twelve) |1|one|", std_ans.lower()):
                bot.send_message(chat_id, data_dct['voice_proccesing_messages']['at_1_sky']['part_1'], parse_mode='html')

                active_users[user_id]['State'] = 'time_4'
                active_users[user_id]['Question'] = random.choice(data_dct['voice_proccesing_messages']['time_3']['part_1'])

                await bot.send_message(chat_id, active_users[user_id]['Question'], parse_mode='html')
            else:
                await bot.send_message(chat_id,  data_dct['voice_proccesing_messages']['time_1']['part_3'], parse_mode='html')

        elif user_state == 'time_4':
            std_ans = await get_student_voice_and_transcribe(message)   # to do
            comm_fr_gpt = await check_student_time_7(std_ans, active_users[user_id]['Question'])
            print('Student answer: ', std_ans)
            print('Commentary from gpt: ', comm_fr_gpt)
            # await save_db(user_id, chat_id, username)

            await send_message_as_a_voice(message, comm_fr_gpt, 'murf')

            if re.search("", std_ans.lower()):
                start_message = data_dct['voice_proccesing_messages']['time_1']['part_1']

                await bot.send_message(chat_id, start_message, parse_mode='html')

                active_users[user_id]['State'] = 'time_5'
                active_users[user_id]['Question'] = await random.choice(data_dct['voice_proccesing_messages']['time_4']['part_1'])

                await bot.send_message(chat_id, active_users[user_id]['Question'], parse_mode='html')

            else:
                bot.send_message(message.chat.id, data_dct['voice_proccesing_messages']['time_1']['part_3'], parse_mode='html')


        elif user_state == 'time_5':
            std_ans = await get_student_voice_and_transcribe(message)   # to do
            comm_fr_gpt = await check_student_time_7(std_ans, active_users[user_id]['Question'])
            print('Student answer: ', std_ans)
            print('Commentary from gpt: ', comm_fr_gpt)
            # await save_db(user_id, chat_id, username)

            await send_message_as_a_voice(message, comm_fr_gpt, 'murf')

            if re.search("", std_ans.lower()):
                active_users[user_id]['State'] = 'time_6'
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_1']['part_1'], parse_mode='html')

                active_users[user_id]['Question'] = await random.choice(data_dct['voice_proccesing_messages']['time_5']['part_2'])
                await bot.send_message(chat_id, '🎙👉🏻 Record voice: ' + active_users[user_id]['Question'], parse_mode='html')

            else:
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_5']['part_1'], parse_mode='html')

        elif active_users[message.from_user.id]['State'] == 'time_6':
            std_ans = await get_student_voice_and_transcribe(message)   # to do
            comm_fr_gpt = await check_student_time_7(std_ans, active_users[user_id]['Question'])
            print('Student answer: ', std_ans)
            print('Commentary from gpt: ', comm_fr_gpt)
            # await save_db(user_id, chat_id, username)

            await send_message_as_a_voice(message, comm_fr_gpt, 'murf')

            if re.search("", std_ans.lower()):
                active_users[user_id]['State'] = 'time_7'
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_1']['part_1'], parse_mode='html')

                active_users[user_id]['Question'] = await random.choice(data_dct['voice_proccesing_messages']['time_6']['part_1'])
                await bot.send_message(chat_id, '🎙👉🏻 Record voice: ' + active_users[user_id]['Question'], parse_mode='html')

            else:
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_1']['part_3'], parse_mode='html')
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_6']['part_2'], parse_mode='html')


        elif active_users[user_id]['State'] == 'time_7':
            std_ans = await get_student_voice_and_transcribe(message)   # to do
            comm_fr_gpt = await check_student_time_7(std_ans, active_users[user_id]['Question'])
            print('Student answer: ', std_ans)
            print('Commentary from gpt: ', comm_fr_gpt)
            # await save_db(user_id, chat_id, username)

            await send_message_as_a_voice(message, comm_fr_gpt, 'murf')

            if re.search("", std_ans.lower()):
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_1']['part_1'], parse_mode='html')
                active_users[user_id]['State'] = 'time_8'

                active_users[user_id]['Question'] = await random.choice(data_dct['voice_proccesing_messages']['time_7']['part_1'])
                await bot.send_message(chat_id, '🎙👉🏻 Record voice: ' + active_users[user_id]['Question'], parse_mode='html')

            else:
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_0']['part_2'], parse_mode='html')
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_7']['part_2'], parse_mode='html')

        elif user_state == 'time_8':
            std_ans = await get_student_voice_and_transcribe(message)   # to do
            comm_fr_gpt = await check_student_time_7(std_ans, active_users[user_id]['Question'])
            print('Student answer: ', std_ans)
            print('Commentary from gpt: ', comm_fr_gpt)
            # await save_db(user_id, chat_id, username)

            await send_message_as_a_voice(message, comm_fr_gpt, 'murf')

            if re.search("", std_ans.lower()):
                active_users[user_id]['State'] = 'time_9'
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_8']['part_1'], parse_mode='html')

                active_users[user_id]['Question'] = random.choice(data_dct['voice_proccesing_messages']['time_8']['part_2'])
                await bot.send_message(chat_id, '🎙👉🏻 Record voice: ' + active_users[user_id]['Question'], parse_mode='html')

            else:
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_0']['part_2'], parse_mode='html')


        elif user_state == 'time_9':
            std_ans = await get_student_voice_and_transcribe(message)   # to do
            comm_fr_gpt = await check_student_time_7(std_ans, active_users[user_id]['Question'])
            print('Student answer: ', std_ans)
            print('Commentary from gpt: ', comm_fr_gpt)
            # await save_db(user_id, chat_id, username)

            await send_message_as_a_voice(message, comm_fr_gpt, 'murf')

            if re.search("", std_ans.lower()):
                active_users[user_id]['State'] = 'time_10'
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_9']['part_1'], parse_mode='html')

                active_users[user_id]['Question'] = random.choice(data_dct['voice_proccesing_messages']['time_9']['part_2'])
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_9']['part_2'] + '🎙👉🏻 Record voice: ' + active_users[user_id]['Question'],
                                parse_mode='html')

            else:
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_0']['part_2'], parse_mode='html')


        elif user_state == 'time_10':
            std_ans = await get_student_voice_and_transcribe(message)   # to do
            comm_fr_gpt = await check_student_time_7(std_ans, active_users[user_id]['Question'])
            print('Student answer: ', std_ans)
            print('Commentary from gpt: ', comm_fr_gpt)
            # await save_db(user_id, chat_id, username)

            await send_message_as_a_voice(message, comm_fr_gpt, 'murf')

            if re.search("", std_ans.lower()):
                active_users[user_id]['State'] = ''

                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_1']['part_1'], parse_mode='html')
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_10']['part_1'], parse_mode='html')

            else:
                await bot.send_message(chat_id, data_dct['voice_proccesing_messages']['time_0']['part_2'], parse_mode='html')




def register_handlers_voice_process(dp):
    dp.register_message_handler(voice_processing, content_types=['voice'])