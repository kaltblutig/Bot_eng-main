from data.interview_data import active_users_interview, interivew_python_questions, interview_dct
from services.service_interview import check_user_exist_or_create, print_user_info, interview_finish, paraphrase, paraphrase_requestes, check_student_answer, check_student_code
import datetime
from create_bot import bot
import create_bot
from aiogram import Dispatcher, types
from services.service_common import send_message_as_a_voice
from services.service_voice_proc import get_student_voice_and_transcribe



async def start_interview(message):
    create_bot.TYPE_OF_ACTIVITY = 'Interviews'
  
    user_id = message.from_user.id

    await check_user_exist_or_create(user_id) # заводим нового пользователя

    # создаём идентификатор диалога в момент нажатия Старт
    active_users_interview[user_id]['ConvId'] = '-vanya-'+ str(message.chat.id) + '-' + str(datetime.datetime.now())

    # Добавить про проверку АЯ, когда добавлю в код!!!!
    #If you want us to check your English, type command "english"
    #If you want us to check your code, type command "python"

    await bot.send_message(message.chat.id, interview_dct['start_message'], parse_mode='html')

    # Выбираем рандомный вопрос из списка -- надо переписать под структуру вопросов
    active_users_interview[user_id]['QuesNum'] = 0 #random.randint(0, len(interivew_python_questions) - 1)
    active_users_interview[user_id]['QuesNumsDone'].append(active_users_interview[user_id]['QuesNum'])
    active_users_interview[user_id]['LastQues'] = interivew_python_questions[active_users_interview[user_id]['QuesNum']]
    active_users_interview[user_id]['Dialog'] = active_users_interview[user_id]['Dialog'] + '\n' + 'Question: ' + active_users_interview[user_id]['LastQues']

    await send_message_as_a_voice(message, active_users_interview[user_id]['LastQues'], 'murf')

    #print(active_users[message.from_user.id]['LastQues'])
    
    # bot_properties=bot.get_me() -- запись внутри отправки сообщения
    # botId = bot_properties.id
    # botName = bot_properties.username
    # save_to_db(
    #     conversationId = '-vanya-'+ str(message.chat.id),
    #     userId = botId,
    #     userName = botName,
    #     isStudent = 0,
    #     userSpeechRecordedAt = int(time.time()),
    #     userSpeechRecordFormat = 'mp3',
    #     userSpeech = active_users[message.from_user.id]['LastQues'],
    #     userSpeechRecordPath = "text_to_speech_by_murf"+str(message.from_user.id)+".mp3",
    #     userSpeechRecordFileName = "text_to_speech_by_murf"+str(message.from_user.id)+".mp3",
    # )
    # if os.path.exists("text_to_speech_by_murf"+str(message.from_user.id)+".mp3"):
    #   print('File to DB exist')
    # else: print('No file to DB')

    #print_user_info(message.from_user.id)


async def send_next_question(message): 

    user_id = message.from_user.id

    await check_user_exist_or_create(user_id) # заводим нового пользователя


    #random_index = random.randint(0, len(interivew_python_questions) - 1)
    if len(active_users_interview[user_id]['QuesNumsDone']) < len(interivew_python_questions):
      active_users_interview[user_id]['QuesNum'] += 1
      active_users_interview[user_id]['QuesNumsDone'].append(active_users_interview[user_id]['QuesNum'])
      active_users_interview[user_id]['LastQues'] = interivew_python_questions[active_users_interview[user_id]['QuesNum']]
      active_users_interview[user_id]['Dialog'] = active_users_interview[user_id]['Dialog'] + '\n' + 'Question: ' + active_users_interview[user_id]['LastQues']
      
      await send_message_as_a_voice(message, active_users_interview[user_id]['LastQues'], 'murf')
      #print(active_users[message.from_user.id]['LastQues'])

    else:
      active_users_interview[user_id]['result'] = await interview_finish(active_users_interview[user_id]['StudRate']) 
      #result = "That's all question for you for now. Well done!"
      active_users_interview[user_id]['Dialog'] = active_users_interview[user_id]['Dialog'] + '\n' + 'Result: ' + active_users_interview[user_id]['result']
      
      send_message_as_a_voice(message, active_users_interview[user_id]['result'], 'murf')

      active_users_interview[user_id]['end_message'] = 'Your result is ' + str(active_users_interview[user_id]['StudRate']) + ' of ' + str(len(interivew_python_questions)) + ' with a "pass"-result equals ' + str(InterviewPassedScore)
      
      await bot.send_message(message.chat.id, active_users_interview[user_id]['end_message'], parse_mode='html')

      await bot.send_message(message.chat.id, interview_dct['restart_message'], parse_mode='html')

      print_user_info(user_id) 


async def voice_processing(message: types.audio):
    if create_bot.TYPE_OF_ACTIVITY == 'Interviews':
      user_id = message.from_user.id

      await check_user_exist_or_create(user_id) # заводим нового пользователя

      #student_audio_path = 'last_voice_from_user'+str(message.from_user.id)+'.mp3'
      active_users_interview[user_id]['Student_answer'] = await get_student_voice_and_transcribe(message)
      active_users_interview[user_id]['Dialog'] = active_users_interview[user_id]['Dialog'] + '\n' + 'Answer: ' + active_users_interview[user_id]['Student_answer']

      # save_to_db_fb(
      #   conversationId = active_users_interview[message.from_user.id]['ConvId'],
      #   userId = message.from_user.id,
      #   userName = message.from_user.first_name,
      #   isStudent = 1,
      #   userSpeechRecordedAt = int(time.time()),
      #   userSpeechRecordFormat = 'wav',
      #   userSpeech = active_users_interview[message.from_user.id]['Student_answer'],
      #   userSpeechRecord = active_users_interview[message.from_user.id]['Student_answer'],
      #   #userSpeechRecordPath = 'last_voice_from_user'+str(message.from_user.id)+'.wav',
      #   userSpeechRecordFileName = 'last_voice_from_user'+str(message.from_user.id)+'.wav',
      # ) 
      # #print_user_info(message.from_user.id)         

      active_users_interview[user_id]['NeedRepeat'] = False
      active_users_interview[user_id]['NeedRepeat'] = await paraphrase_requestes(active_users_interview[user_id]['Student_answer'])
      #print(Student_answer + '\n')
      #print('NeedRepeat = ' + str(NeedRepeat))

      if active_users_interview[user_id]['NeedRepeat']:
        active_users_interview[user_id]['QuestionModified'] = await paraphrase(active_users_interview[user_id]['LastQues'])
        await send_message_as_a_voice(message, active_users_interview[user_id]['QuestionModified'], 'murf')
        return 0


      active_users_interview[user_id]['comment_from_GPT'] = await check_student_answer(active_users_interview[user_id]['LastQues'], active_users_interview[user_id]['Student_answer'], user_id) # нужно переписать обработчик: доп.вопросы
      
      await send_message_as_a_voice(message, active_users_interview[user_id]['comment_from_GPT'], 'murf')
      
      await bot.send_message(message.chat.id, interview_dct['go_to_next'], parse_mode='html')    
      #print_user_info(message.from_user.id)

      #Выводить кнопки next|Quit или проговаривать инструкцию к ним чтобы пойти дальше

     
async def text_processing(message):
  if create_bot.TYPE_OF_ACTIVITY == 'Interviews':
    user_id = message.from_user.id

    await check_user_exist_or_create(user_id)
    
    # save_to_db(
    #   conversationId = active_users[message.from_user.id]['ConvId'],
    #   userId = message.from_user.id,
    #   userName = message.from_user.first_name,
    #   isStudent = 1,
    #   userSpeechRecordedAt = int(time.time()),
    #   userSpeechRecordFormat = 'wav',
    #   userSpeech = message.text,
    #   userSpeechRecordPath = '',
    #  userSpeechRecordFileName = '',
    # ) 

    active_users_interview[user_id]['Student_answer'] = message.text
    active_users_interview[user_id]['comment_from_GPT'] = await check_student_code(active_users_interview[user_id]['LastQues'], \
                                                                             active_users_interview[user_id]['Student_answer'], user_id) # нужно переписать обработчик: доп.вопросы
    
    await send_message_as_a_voice(message, active_users_interview[user_id]['comment_from_GPT'], 'murf')
    
    await print_user_info(user_id)

    await bot.send_message(message.chat.id, interview_dct['go_to_next'], parse_mode='html')
    
    #Добавить возможность выводить комментарии текстом или повторять/перефразировать их, если пользователь не понял



def register_handlers_interview_1(dp : Dispatcher):
    dp.register_message_handler(start_interview, commands=['Interviews'])
    dp.register_message_handler(send_next_question, commands=['next'])
    dp.register_message_handler(voice_processing, content_types=['voice'])
    dp.register_message_handler(text_processing, content_types=['text'])

