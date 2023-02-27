import asyncio
from aiogram import Bot
from aiogram.dispatcher import Dispatcher        
import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()  


loop = asyncio.get_event_loop()

TYPE_OF_ACTIVITY = ''

bot = Bot(token=config.TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)   