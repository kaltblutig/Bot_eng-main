from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


but_1 = KeyboardButton('/Lessons')
but_2 = KeyboardButton('/Interviews')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.row(but_1, but_2)

but_less_1 = KeyboardButton('/time')
but_less_2 = KeyboardButton('/email')

kb_client_lessons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client_lessons.row(but_less_1, but_less_2)