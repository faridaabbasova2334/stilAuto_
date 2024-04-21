from aiogram import executor
from create_bot import dp
from handler import client, other
from data_base import sqlite_base


if __name__ == '__main__':
    print('Бот вышел в онлайн')
    sqlite_base.sql_start()
    client.register_handlers_client(dp)
    other.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=True)
