from aiogram.utils import executor      # для того чтобы бот вышел в онлайн
import logging
from create_bot import dp
from handlers import greeting, lesson_time, lesson_email, voice_processing, interview_1
# from database import sqlite_db


logging.basicConfig(level=logging.INFO)


# function for bot when he come up in online
# specifying service information
async def on_startup(_):
    print('Bot in online')
    # sqlite_db.sql_start()


greeting.register_handlers_client(dp)
lesson_time.register_handlers_lesson_time(dp)
lesson_email.register_handlers_lesson_time(dp)
voice_processing.register_handlers_voice_process(dp)
interview_1.register_handlers_interview_1(dp)



# if bot not online he won't get messages after he come up online, skip_updates do this
# skip old incoming updates from queue
# start long_polling it's like launch code that can get actions by users
# function on_startup written at the beginnning of he code 
# на самом деле start_polling делает метод get_updates на сервер телеграма
executor.start_polling(dp, skip_updates=True, on_startup=greeting.send_to_admin_launch)