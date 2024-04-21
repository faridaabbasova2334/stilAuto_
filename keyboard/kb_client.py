from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# start
button1 = KeyboardButton('Добавить сотрудника')
buttonSearchPhoto = KeyboardButton('Найти сотрудника по фото авто')
buttonSearchNumber = KeyboardButton('Найти сотрудника по номеру авто')
kb_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(buttonSearchNumber, button1)

##
kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отмена'))
##
