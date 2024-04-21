from aiogram.dispatcher import Dispatcher
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token='7079343586:AAGGoNKeX2J3uFKfl8U3YIprKf-4clK7Bso')
dp = Dispatcher(bot, storage=storage)
