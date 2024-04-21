from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from keyboard import kb_client
from data_base import sqlite_base
from aiogram.dispatcher.filters import Text
import re


class FSMSearchPhoto(StatesGroup):
    photo = State()


class FSMSearchNumber(StatesGroup):
    number = State()


class FSMAdd(StatesGroup):
    fio = State()
    number = State()
    photo = State()
    telephon = State()
    address = State()


async def command_start(message: types.Message):
    priv = 'Что необходимо?'
    await bot.send_message(message.from_user.id, priv, reply_markup=kb_client.kb_menu)


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await bot.send_message(message.from_user.id, 'Вы ввели что-то не то', reply_markup=kb_client.kb_menu)
        return
    await state.finish()
    await bot.send_message(message.from_user.id, 'Операция отменена', reply_markup=kb_client.kb_menu)


async def searchPhoto(message: types.Message):
    await FSMSearchPhoto.photo.set()
    await bot.send_message(message.from_user.id, "Отправьте фото", reply_markup=kb_client.kb_cancel)



async def add_sotrudnik(message: types.Message):
    await FSMAdd.fio.set()
    await bot.send_message(message.from_user.id, "Введите имя", reply_markup=kb_client.kb_cancel)


async def loadFIO(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fio'] = message.text
    await FSMAdd.next()
    await bot.send_message(message.from_user.id, "Введите номер авто и регион. Пример: а000аа126")


async def loadNumber(message: types.Message, state: FSMContext):
    # Регулярное выражение(Regular Expression)
    pattern = r'\b[АВЕКМНОРСТУХABEKMHOPCTYX]{1}\d{3}[АВЕКМНОРСТУХABEKMHOPCTYX]{2}\d{2,3}\b'
    if re.fullmatch(pattern, message.text, re.IGNORECASE):
        async with state.proxy() as data:
            data['number'] = message.text.upper().replace(" ", "")
        await FSMAdd.next()
        await bot.send_message(message.from_user.id, "Отправте фото авто")
    else:
        await message.reply("Вы ввели не верный номер авто. Попробуйте ещё раз")


async def loadPhoto(message: types.Message, state: FSMContext):
    if message.content_type == 'photo':
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdd.next()
        await bot.send_message(message.from_user.id, "Введите номер телефона")
    else:
        pass


async def loadTelephon(message: types.Message, state: FSMContext):
    text = message.text
    if re.findall("[0-9.+]", text) == list(text) and len(re.findall("[0-9.+]", text)) < 13 and len(
            re.findall("[0-9.+]", text)) > 10:
        async with state.proxy() as data:
            data['telephon'] = message.text
        await FSMAdd.next()
        await bot.send_message(message.from_user.id, "Отправьте ссылку на ваш аккаунт в формате t.me/name_account")
    else:
        await message.reply("Вы не верно ввели номер телефона. Попробуйте еще раз")


async def loadAddres(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    await sqlite_base.sotrudniki(state)
    await bot.send_message(message.from_user.id, 'Добавлено в базу', reply_markup=kb_client.kb_menu)
    await state.finish()


async def searchNumber(message: types.Message):
    await FSMSearchNumber.number.set()
    await bot.send_message(message.from_user.id, "Введите номер авто и регион. Пример: а000аа126", reply_markup=kb_client.kb_cancel)


async def readNumber(message: types.Message, state: FSMContext):
    data = message.text.upper()
    await sqlite_base.sotrudniki_read(message, data)
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(cancel_handler, Text(equals=['отмена'], ignore_case=True), state="*")
    dp.register_message_handler(add_sotrudnik, Text(equals=['добавить сотрудника'], ignore_case=True))
    dp.register_message_handler(searchNumber, Text(equals=['найти сотрудника по номеру авто'], ignore_case=True))
    dp.register_message_handler(searchPhoto, Text(equals=['Найти сотрудника по фото авто'], ignore_case=True))
    dp.register_message_handler(loadFIO, state=FSMAdd.fio)
    dp.register_message_handler(loadNumber, state=FSMAdd.number)
    dp.register_message_handler(loadPhoto, content_types=['photo'], state=FSMAdd.photo)
    dp.register_message_handler(loadTelephon, state=FSMAdd.telephon)
    dp.register_message_handler(loadAddres, state=FSMAdd.address)
    dp.register_message_handler(readNumber, state=FSMSearchNumber.number)
