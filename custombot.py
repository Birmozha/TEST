import sqlite3

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text

from config import TOKEN


# ПОПЫТКА СОЗДАТЬ ОБЪЕКТЫ, УНАСЛЕДОВАННЫЕ ОТ ОБЪЕКТОВ AIOGRAM

class CustomKeyboardButton(KeyboardButton):
    hidden_id = None


bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    print('---------')
    print(message)
    print('---------')
    await message.answer(text='Привет', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(CustomKeyboardButton(text='Какой-то текст', hidden_id=15)))

@dp.message_handler()
async def other(message: types.Message):
    print('---------')
    print(message)
    print('---------')
    await message.answer(text=message.text)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
