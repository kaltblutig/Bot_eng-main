from data.data_for_lessons import active_users
import requests
import json
import urllib
from create_bot import bot
from gtts import gTTS
import aiofiles
from config import FLAG


# проверка на наличие юзера в нашей структуре -> to do: db mysql + aio, more effective checking
async def check_user_exist_or_create(user_id):
  try:
      active_users[user_id]
  except:
      active_users[user_id] = {
          'Dialog': '',
          'Student_answer': '',
          'Bot_last_comment': '',
          'Student_last_comment': '',
          'State': 'Please, use command / start or wait the answer',
          'Main_prompt': '',
          'save_path': '',
          'temp': '',
          'Question': '',
      }
  return



async def text_to_speech_by_murf(text_to, user_id) -> str:
  """
  Функция перевод текст в аудио и возвращет строку, что является названием аудио,
  которое озвучивает текст.
  """
  CHOSEN_VOICE = 'en-US-brianna'
  FORMAT = 'MP3'
  
  # getting token from api_key
  url = 'https://api.murf.ai/v1/auth/token'
  headers = {'api-key': 'api_826c96cf-fdfe-47d2-a6a7-1790cfe67a07'}
  
  response = requests.get(url=url, headers=headers) # return token
  response = json.loads(response.text)
  
  token = response['token']
  
  # getting list of voices
  headers={'token': token}
  url='https://api.murf.ai/v1/speech/voices'
  
  response = requests.get(url=url, headers=headers)
  response = json.loads(response.text)
  
  headers = {'token': token, 'Content-Type': 'application/json'}
  
  data = {
        "text": text_to,
        "voiceId": CHOSEN_VOICE,
        "format": FORMAT,
        "channelType": "MONO",
        "sampleRate": "24000"
    }
  
  url = 'https://api.murf.ai/v1/speech/generate'
  
  response = requests.post(url=url, headers=headers, json=data)
  response = json.loads(response.text)
  
  url_to_audio = response['audioFile']
  
  urllib.request.urlretrieve(url_to_audio, f'text_to_speech_by_murf' + str(user_id) + '.mp3')

  return 'text_to_speech_by_murf' + str(user_id) + '.mp3'


# отправляем  аудио сообщение
async def send_message_as_a_voice(message, bot_last_comment, voice_type):
  # print('send_mess_as_voice_args: ', message, bot_last_comment, voice_type, flag)
  if voice_type == 'murf':
    answer_audio_place = await text_to_speech_by_murf(bot_last_comment, message.from_user.id)
    await bot.send_voice(message.chat.id, open(answer_audio_place, 'rb'))
    
    bot_properties = await bot.get_me()
    bot_id = bot_properties.id
    bot_name = bot_properties.username
    
    # save_to_db(
    # conversationId = active_users[message.from_user.id]['ConvId'],
    # userId = bot_id,
    # userName = bot_name,
    # isStudent = 0,
    # userSpeechRecordedAt = int(time.time()),
    # userSpeechRecordFormat = 'mp3',
    # userSpeech = active_users[message.from_user.id]['LastQues'],
    # userSpeechRecordPath = "text_to_speech_by_murf"+str(message.from_user.id)+".mp3",
    # userSpeechRecordFileName = "text_to_speech_by_murf"+str(message.from_user.id)+".mp3",
    #   )

    # if os.path.exists("text_to_speech_by_murf"+str(message.from_user.id)+".mp3"):
    #   print('File to DB exist')
    # else: print('No file to DB')
    
  if voice_type == 'gtts':  
    output = gTTS(bot_last_comment, lang = 'en', slow = False)
    output.save('sent_message_audio' + str(message.from_user.id) + '.wav')
    sent_message_audio = open('sent_message_audio' + str(message.from_user.id) + '.wav', 'rb')
    
    await bot.send_voice(message.chat.id, sent_message_audio)
    
  if voice_type == 'facebook':

    if FLAG == 'prod':
        fixed_text = bot_last_comment.replace('. ', '.,, ').replace(' and ', ', and').replace(' but ',', but ').replace(' howether ',', howether ').replace('?','?,').replace(':',' ').replace('!','!,')
        headers = {'Username': 'abc@gmail.com', 'apikey':'123-456'}
        payload = {'text': fixed_text}
        resp = await requests.post("http://sel3-common-ml-2.skyeng.link:8010", json=payload, headers=headers)
        result = resp.content
        await bot.send_audio(message.chat.id, result)
    elif FLAG == 'dev':
        async with aiofiles.open('sample.mp3', 'rb') as audio:
            await bot.send_audio(message.chat.id, audio)
            
    #   bot_properties=bot.get_me()
    #   bot_id = bot_properties.id
    #   bot_name = bot_properties.username
      # save_to_db_fb(
      #     conversationId = active_users[message.from_user.id]['ConvId'],
      #     userId = botId,
      #     userName = botName,
      #     isStudent = 0,
      #     userSpeechRecordedAt = int(time.time()),
      #     userSpeechRecordFormat = 'wav',
      #     userSpeech = active_users[message.from_user.id]['LastQues'],
      #     userSpeechRecord = result,
      #     userSpeechRecordFileName = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+'-IvanBot-'+str(message.from_user.id)+'.wav',
      # )
      
      # if os.path.exists("text_to_speech_by_murf"+str(message.from_user.id)+".mp3"):
      #   print('File to DB exist')
      # else: print('No file to DB')
  
  # return 'ok'