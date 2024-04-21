import sqlite3 as sq
from create_bot import bot
from keyboard import kb_client
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def sql_start():
    global base, cur
    base = sq.connect('Sotrudnikii.db')
    cur = base.cursor()
    if base:
        print('Base connected')
    base.execute('CREATE TABLE IF NOT EXISTS сотрудники'
                 '(fio TEXT, number TEXT PRIMARY KEY, photo TEXT, telephon TEXT, address TEXT)')
    base.commit()


async def sotrudniki(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO сотрудники VALUES (?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sotrudniki_read(message, data):
    if cur.execute('SELECT * FROM сотрудники WHERE number == ?', (data,)).fetchall():
        for ret in cur.execute('SELECT * FROM сотрудники WHERE number == ?', (data,)).fetchall():
            await bot.send_photo(message.from_user.id, ret[2])
            await bot.send_message(message.from_user.id, f"Имя: {ret[0]}\nНомер авто: {ret[1]}\nТелефон владельца: {ret[3]}\nСсылка на аккаунт: {ret[4]}", reply_markup=kb_client.kb_menu)
    else:
        await bot.send_message(message.from_user.id, "Такого номера нет в базе", reply_markup=kb_client.kb_menu)
