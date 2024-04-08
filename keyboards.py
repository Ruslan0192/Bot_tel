
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
# first = ReplyKeyboardMarkup(resize_keyboard=True)
# first.add('начинаем')

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Начать расчет')
# main.add('Начать расчет').add('Задать вопрос')

# user_panel = ReplyKeyboardMarkup(resize_keyboard=True)
# user_panel.add('Ввести параметры заново').add('Задать вопрос')

user_pay = ReplyKeyboardMarkup(resize_keyboard=True)
user_pay.add('Оплатить')
# user_pay.add('Оплатить').add('Ввести параметры заново').add('Задать вопрос')

user_recalc = ReplyKeyboardMarkup(resize_keyboard=True)
user_recalc.add('Загрузить файл повторно')
# user_recalc.add('Загрузить файл повторно').add('Сделать новый расчет').add('Задать вопрос')

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Админ-панель')


# catalog_list = InlineKeyboardMarkup(row_width=2)
# catalog_list.add(InlineKeyboardButton(text='Футболки', callback_data='t-shirt'),
#                  InlineKeyboardButton(text='Шорты', callback_data='shorts'),
#                  InlineKeyboardButton(text='Кроссовки', callback_data='sneakers'))

cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add('Отмена')