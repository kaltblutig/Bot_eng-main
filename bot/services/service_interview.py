from data.prompts import prompts_dct
from data.interview_data import active_users_interview
import openai
from data.interview_data import interview_passed_score


# Ученик не понял вопрос?
async def paraphrase_requestes(answer):
    prompt = prompts_dct['interview_1_prompts']['paraphrase_requestes'] + '\n' + 'Answer: ' + answer + '\n' + 'UnderstandingCheck: '
    
    try:
        response = openai.Completion.create(engine="text-davinci-003", prompt = prompt, max_tokens=250, temperature=0.7) #max_tokens=5
    except Exception as ex:
        print(ex)  

    response_text_string = response['choices'][0]['text']

    return (response_text_string == " Yes") or (response_text_string == " yes")


# Переформулировка вопроса
async def paraphrase(question):    
    prompt = prompts_dct['interview_1_prompts']['paraphrase'] + 'Question: ' + question

    try:
        response = openai.Completion.create(engine="text-davinci-003", prompt = prompt, max_tokens=250, temperature=0.7) #max_tokens=5
    except Exception as ex:
        print(ex)  

    response_text_string = response['choices'][0]['text']

    return response_text_string


async def interview_finish(std_rate):
    if std_rate >= interview_passed_score:
      pre_prompt = prompts_dct['interview_1_prompts']['interview_finish']['1_pre_prompt']
    else:
      pre_prompt = prompts_dct['interview_1_prompts']['interview_finish']['2_pre_prompt']
    
    try:
        response = openai.Completion.create(engine="text-davinci-003", prompt = pre_prompt, max_tokens=250, temperature=0.7) #max_tokens=5
    except Exception as ex:
        print(ex)    

    response_text_string = response['choices'][0]['text']

    return response_text_string


# Проверяем ответ студента в общем случае
async def check_student_answer(qst, ans, user_id): #Здесь поправить промт для того, что проверять в ответе У
    await check_user_exist_or_create(user_id)
    
    pre_prompt = prompts_dct['interview_1_prompts']['check_student_answer']
    prompt = pre_prompt + '\n' + 'Question: ' + qst + '\n' + 'Answer: ' + ans + '\n' + 'Comment: '

    try:
        response = openai.Completion.create(engine="text-davinci-003", prompt = prompt, max_tokens=250, temperature=0.7) #max_tokens=5
    except Exception as ex:
        print(ex) 

    response_text_string = response['choices'][0]['text']
    #print(prompt + '\n\n' + response_text_string)

    # Накидываем балл за правильный код
    if 'Yes' in response_text_string:
      active_users_interview[user_id]['StudRate'] += 1
    
    return response_text_string


# Здесь проверяем ответ студента, если ответ текстовый = код
async def check_student_code(qst, ans, user_id): #Здесь поправить промт для того, что проверять в ответе У
    await check_user_exist_or_create(user_id)

    pre_prompt = prompts_dct['interview_1_prompts']['check_student_code']
    prompt = pre_prompt + '\n' + 'Question: ' + qst + '\n' + 'Answer: ' + ans + '\n' + 'Comment: '
    try:
        response = openai.Completion.create(engine="text-davinci-003", prompt = prompt, max_tokens=250, temperature=0.7) #max_tokens=5
    except Exception as ex:
        print(ex) 

    response_text_string = response['choices'][0]['text']
    #print(prompt + '\n\n' + response_text_string)

    # Накидываем балл за правильный код
    if 'Yes' in response_text_string:
      active_users_interview[user_id]['StudRate'] += 1
    
    return response_text_string



# Проверка существования пользователя чата
async def check_user_exist_or_create(user_id):
  try: 
    active_users_interview[user_id]
  except:
      active_users_interview[user_id] = {
          'Dialog': '',
          'Student_answer': '',
          'Bot_last_comment': '',
          'Student_last_comment': '',
          'State': '1',
          'Main_prompt': '',
          'StudRate': 0,
          'LastQues': '',
          'QuesNum': 0,
          'QuesNumsDone': [],
          'result': '',
          'end_message': '',
          'NeedRepeat': False,
          'QuestionModified': '',
          'comment_from_GPT': '',
          'ConvId': ''
          }
  return


async def print_user_info(user_id):
  print('Dialog = ' + active_users_interview[user_id]['Dialog'] + '\n')
  print('Student_answer = ' + active_users_interview[user_id]['Student_answer'] + '\n')
  print('Bot_last_comment = ' + active_users_interview[user_id]['Bot_last_comment'] + '\n')
  print('Student_last_comment = ' + active_users_interview[user_id]['Student_last_comment'] + '\n')
  print('Main_prompt = ' + active_users_interview[user_id]['Main_prompt'] + '\n')
  print('StudRate = ' + str(active_users_interview[user_id]['StudRate']) + '\n')
  print('LastQues = ' + active_users_interview[user_id]['LastQues'] + '\n')
  print('QuesNum = ' + str(active_users_interview[user_id]['QuesNum']) + '\n')
  #print('QuesNumsDone = ' + active_users[user_id]['QuesNumsDone'] + '\n')
  print('result = ' + active_users_interview[user_id]['result'] + '\n')
  print('end_message = ' + active_users_interview[user_id]['end_message'] + '\n')
  #print('NeedRepeat = ' + active_users[user_id]['DialNeedRepeatog'] + '\n')
  print('QuestionModified = ' + active_users_interview[user_id]['QuestionModified'] + '\n')
  print('comment_from_GPT = ' + active_users_interview[user_id]['comment_from_GPT'] + '\n')
  
  return