from aiogram import types, Dispatcher
from create_bot import bot
import os


async def text(message: types.Message):
    if message.content_type != 'photo':
        await bot.send_message(message.from_user.id, 'Вы ввели что-то не то')
        return
    photo = message.photo[-1]  # Берем последнюю (наибольшего размера) фотографию
    photo_id = photo.file_id

    # Загружаем фото в директорию проекта
    await bot.download_photo(photo_id, os.path.join('photos', f'{photo_id}.jpg'))
    # await bot.send_message(message.from_user.id, "alksdklawd")
    # photo = message.photo[-1]  # Получаем последнее (наибольшее по размеру) изображение
    # await bot.send_message(message.from_user.id, "alksdklawd")
    # file_id = photo.file_id
    # await bot.send_message(message.from_user.id, "alksdklawd")
    # file = await bot.download_file(file_id)
    # await bot.send_message(message.from_user.id, "alksdklawd")
    # with open(f"downloaded_image.jpg", 'wb') as new_file:
    #     new_file.write(file.read())
    # await bot.send_message(message.from_user.id, "alksdklawd")


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(text)
