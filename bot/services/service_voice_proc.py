from data.data_for_lessons import data_dct, active_users
from data.prompts import prompts_dct
from .service_common import check_user_exist_or_create
from create_bot import bot
import aiofiles
import requests
import json
import openai 
from config import FLAG
import whisper
from pathlib import Path


OpenAI_API_KEY = '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'  # To English_Topic_Bot
openai.api_key = OpenAI_API_KEY


async def get_student_voice_and_transcribe_wym(message) -> str:
    user_id = message.from_user.id

    await check_user_exist_or_create(user_id)

    if FLAG == 'prod':
        # А теперь в виде API
        file_info = await bot.get_file(message.voice.file_id)   # -> {"file_id": "AwACAgIAAxkBAAIBk2P6ZZZdU7RrWz3yCx9rWlLFeOIVAAI-IwAClOPZS4KFJvOwR1GDLgQ", "file_unique_id": "AgADPiMAApTj2Us", "file_size": 7986, "file_path": "voice/file_9.oga"}
        downloaded_file = await bot.download_file(file_info.file_path)  # -> <_io.BytesIO object at 0x10739bc40>

        last_voice_from_user = 'last_voice_from_user' + str(user_id) + '.wav'

        async with aiofiles.open(last_voice_from_user, 'wb') as new_file:
            new_file.write(downloaded_file)

        headers = {'Username': 'abc@gmail.com', 'apikey': '123-456', 'params': 'file_inference,-1'}
        payload = [('file', downloaded_file)]
        resp = requests.post("http://sel3-common-ml-2.skyeng.link:8001", files=payload, headers=headers)
        resp = json.loads(resp.text)
        student_answer = ' '.join([x[0] for x in resp['result']])

    elif FLAG == 'dev':
        voice = await message.voice.get_file()
        path = 'here/'

        Path(f'{path}').mkdir(parents=True, exist_ok=True)
        downloaded_file = await bot.download_file(file_path=voice.file_path, destination=f'{path}/{voice.file_id}.ogg')

        model = whisper.load_model('base')
        result = model.transcribe(f'{path}/{voice.file_id}.ogg', fp16=False)
        student_answer = result['text']

    active_users[user_id]['Student_answer'] = student_answer.lower()
    student_answer = student_answer.replace('com.', 'com')
    student_answer = student_answer.replace('at', '@')
    student_answer = student_answer.replace(' ', '')
    student_answer = student_answer.replace('dot', '.')

    active_users[user_id]['Dialog'] = active_users[user_id]['Dialog'] + '\n' + "Student" + ': ' + student_answer

    return student_answer


async def check_student_said_at(ans) -> str:
    pre_prompt = prompts_dct['service_2']['check_student_said_at']

    prompt = pre_prompt + '\n Student:' + ans + '\n' + 'Comment: ' + '\n'

    try:
        response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=150, stop='\n', top_p=0.25)
    except Exception as ex:
        print(ex)
        
    # print(response)
        
    response_text_string = response['choices'][0]['text']
    
    return response_text_string


async def check_student_said_sky_correct(ans):
    pre_prompt = prompts_dct['service_2']['check_student_said_sky_correct']
    prompt = pre_prompt + '\n Student:' + ans + '\n' + 'Comment: ' + '\n'

    try:
        response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=150, stop='\n', top_p=0.25)
    except Exception as ex:
        print(ex)
        
    response_text_string = response['choices'][0]['text']
    
    return response_text_string


async def check_student_time_0(ans):
    pre_prompt = prompts_dct['service_2']['check_student_time_0']
    prompt = pre_prompt + '\n Student:' + ans + '\n' + 'Comment: ' + '\n'

    try:
        response = await openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=150, stop='\n', top_p=0.25)
    except Exception as ex:
        print(ex)
        
    response_text_string = response['choices'][0]['text']

    return response_text_string


async def check_student_time_1(ans, qst):
    pre_prompt = prompts_dct['service_2']['check_student_time_1']
    prompt = pre_prompt + '\n' + qst + '\n Student:' + ans + '\n' + 'You: ' + '\n'

    try:
        response = await openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=150, stop='\n', top_p=0.25)
    except Exception as ex:
        print(ex)
        
    response_text_string = response['choices'][0]['text']
    
    return response_text_string


async def check_student_time_2(ans, qst):
    pre_prompt = prompts_dct['service_2']['check_student_time_2']
    prompt = pre_prompt + '\n' + qst + '\n Student:' + ans + '\n' + 'You: ' + '\n'

    try:
        response = await openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=150, stop='\n', top_p=0.25)
    except Exception as ex:
        print(ex)
        
    response_text_string = response['choices'][0]['text']
   
    return response_text_string


async def check_student_time_4(ans, qst):
    pre_prompt = prompts_dct['service_2']['check_student_time_4']
    prompt = pre_prompt + '\n' + qst + '\n Student:' + ans + '\n' + 'You: ' + '\n'

    try:
        response = await openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=150, stop='\n', top_p=0.25)
    except Exception as ex:
        print(ex)
    
    response_text_string = response['choices'][0]['text']
    
    return response_text_string


async def check_student_time_7(ans, qst):
    pre_prompt = prompts_dct['service_2']['check_student_time_7']
    prompt = pre_prompt + '\n' + qst + '\n Student:' + ans + '\n' + 'You: ' + '\n'

    try:
        response = await openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=150, stop='\n', top_p=0.25)
    except Exception as ex:
        print(ex)
    
    response_text_string = response['choices'][0]['text']
    
    return response_text_string


async def get_student_voice_and_transcribe(message):

    user_id = message.from_user.id

    await check_user_exist_or_create(user_id)

    file_info = await bot.get_file(message.voice.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    last_voice_from_user = 'last_voice_from_user' + str(user_id) + '.wav'

    async with aiofiles.open(last_voice_from_user, 'wb') as new_file:
        new_file.write(downloaded_file)

    if FLAG == 'prod':
        # А теперь в виде API
        file_info = await bot.get_file(message.voice.file_id)   # -> {"file_id": "AwACAgIAAxkBAAIBk2P6ZZZdU7RrWz3yCx9rWlLFeOIVAAI-IwAClOPZS4KFJvOwR1GDLgQ", "file_unique_id": "AgADPiMAApTj2Us", "file_size": 7986, "file_path": "voice/file_9.oga"}
        downloaded_file = await bot.download_file(file_info.file_path)  # -> <_io.BytesIO object at 0x10739bc40>

        last_voice_from_user = 'last_voice_from_user' + str(user_id) + '.wav'

        async with aiofiles.open(last_voice_from_user, 'wb') as new_file:
            new_file.write(downloaded_file)

        headers = {'Username': 'abc@gmail.com', 'apikey': '123-456', 'params': 'file_inference,-1'}
        payload = [('file', downloaded_file)]
        resp = requests.post("http://sel3-common-ml-2.skyeng.link:8001", files=payload, headers=headers)
        resp = json.loads(resp.text)
        student_answer = ' '.join([x[0] for x in resp['result']])

    elif FLAG == 'dev':
        voice = await message.voice.get_file()
        path = 'here/'

        Path(f'{path}').mkdir(parents=True, exist_ok=True)
        downloaded_file = await bot.download_file(file_path=voice.file_path, destination=f'{path}/{voice.file_id}.ogg')

        model = whisper.load_model('base')
        result = model.transcribe(f'{path}/{voice.file_id}.ogg', fp16=False)
        student_answer = result['text']

    active_users[user_id]['Student_answer'] = student_answer.lower()
    student_answer = student_answer.replace('com.', 'com')
    bot.send_message(message.chat.id, 'You mean: ' + student_answer.lower(), parse_mode='html')

    active_users[user_id]['Dialog'] = active_users[user_id]['Dialog'] + '\n' + "Student" + ': ' + student_answer

    return student_answer.lower()