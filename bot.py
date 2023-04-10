from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text

import sqlite3

TOKEN = ''
ADMINS = []

bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    with sqlite3.connect('data.db') as db:
        cur = db.cursor()
        qid = cur.execute(
            """SELECT qid FROM tree WHERE pid IS NULL and properties is '<text>' """
            ).fetchone()[0]
        text = cur.execute(
            """SELECT text FROM data WHERE qid IS (?) """, (qid, )
            ).fetchone()[0]

        bid = cur.execute(
            """SELECT qid, properties FROM TREE WHERE pid IS (?) AND properties LIKE '<button%' """, (qid, )
            ).fetchall()
        ikbs = []
        kbs = []
        for id, prop in bid:
            if prop == '<button:ikb>':
                ikbs.append(cur.execute(
                    """SELECT text, qid FROM data WHERE qid IS (?) """, (id, )
                    ).fetchone())
            else:
                kbs.append(cur.execute(
                    """SELECT text FROM data WHERE qid IS (?) """, (id, )
                    ).fetchone())
    
    if ikbs:
        buttonsText = [button for button in ikbs]
        kb = InlineKeyboardMarkup(row_width=1).add(*[InlineKeyboardButton(text=text, callback_data=qid) for text, qid in buttonsText])
        await message.answer(text=text, reply_markup=kb)
    elif kbs:
        buttonsText = [button[0] for button in kbs]
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*[KeyboardButton(text=text) for text in buttonsText])
        await message.answer(text=text, reply_markup=kb)
    else:
        await message.answer(text=text)

@dp.callback_query_handler()
async def dialog(callback: types.CallbackQuery):
    await callback.answer()
    with sqlite3.connect('data.db') as db:
        cur = db.cursor()
        qid = cur.execute(
            """SELECT qid FROM tree WHERE pid IS (?) and properties is '<text>' """, (callback.data, )
            ).fetchone()[0]
        text = cur.execute(
            """SELECT text FROM data WHERE qid IS (?) """, (qid, )
            ).fetchone()[0]

        bid = cur.execute(
            """SELECT qid, properties FROM TREE WHERE pid IS (?) AND properties LIKE '<button%' """, (qid, )
            ).fetchall()
        ikbs = []
        kbs = []
        for id, prop in bid:
            if prop == '<button:ikb>':
                ikbs.append(cur.execute(
                    """SELECT text, qid FROM data WHERE qid IS (?) """, (id, )
                    ).fetchone())
            else:
                kbs.append(cur.execute(
                    """SELECT text FROM data WHERE qid IS (?) """, (id, )
                    ).fetchone())
    
    if ikbs:
        buttonsText = [button for button in ikbs]
        kb = InlineKeyboardMarkup(row_width=1).add(*[InlineKeyboardButton(text=text, callback_data=qid) for text, qid in buttonsText])
        await callback.message.answer(text=text, reply_markup=kb)

    elif kbs:
        buttonsText = [button[0] for button in kbs]
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*[KeyboardButton(text=text) for text in buttonsText])
        await callback.message.answer(text=text, reply_markup=kb)
    else:
        await callback.message.answer(text=text)


@dp.message_handler()
async def dialog(message: types.Message):
    with sqlite3.connect('data.db') as db:
        cur = db.cursor()
        temp = cur.execute(
            """SELECT qid FROM data WHERE text is (?) """, (message.text, )
        ).fetchone()[0]
        qid = cur.execute(
            """SELECT qid FROM tree WHERE pid IS (?) and properties is '<text>' """, (temp, )
            ).fetchone()[0]
        text = cur.execute(
            """SELECT text FROM data WHERE qid IS (?) """, (qid, )
            ).fetchone()[0]
        
        bid = cur.execute(
            """SELECT qid, properties FROM TREE WHERE pid IS (?) AND properties LIKE '<button%' """, (qid, )
            ).fetchall()
        ikbs = []
        kbs = []
        for id, prop in bid:
            if prop == '<button:ikb>':
                ikbs.append(cur.execute(
                    """SELECT text, qid FROM data WHERE qid IS (?) """, (id, )
                    ).fetchone())
            else:
                kbs.append(cur.execute(
                    """SELECT text FROM data WHERE qid IS (?) """, (id, )
                    ).fetchone())
    
    if ikbs:
        buttonsText = [button for button in ikbs]
        kb = InlineKeyboardMarkup(row_width=1).add(*[InlineKeyboardButton(text=text, callback_data=qid) for text, qid in buttonsText])
        await message.answer(text=text, reply_markup=kb)

    elif kbs:
        buttonsText = [button[0] for button in kbs]
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*[KeyboardButton(text=text) for text in buttonsText])
        await message.answer(text=text, reply_markup=kb)
    else:
        await message.answer(text=text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
