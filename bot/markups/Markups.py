from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

bks_btn = InlineKeyboardButton(text='📉 БКС Брокер', callback_data='bks')
open_btn = InlineKeyboardButton(text='🧾 Открытие', callback_data='open')
vtb_btn = InlineKeyboardButton(text='📈 ВТБ Капитал Форекс', callback_data='vtb')
tnkf_btn = InlineKeyboardButton(text='📒 Тинькофф Инвестиции', callback_data='tnkf')
alfa_btn = InlineKeyboardButton(text='📕 Альфа Инвестиции', callback_data='alfa')
finam_btn = InlineKeyboardButton(text='📋 Финам', callback_data='finam')
freadom_btn = InlineKeyboardButton(text='💹 Фридом Финанс', callback_data='freadom')
capital_btn = InlineKeyboardButton(text='📰 IT Capital', callback_data='capital')

Keyboard_inline = InlineKeyboardMarkup().add(bks_btn, open_btn, vtb_btn, tnkf_btn, alfa_btn, finam_btn, freadom_btn, capital_btn)
# ----Main_menu----

user_btn = KeyboardButton('🆕 Карточка клиента')
help_btn = KeyboardButton('📕 Помощь')
join_btn = KeyboardButton('💵 Получить услугу')
main_Menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(user_btn, help_btn).insert(join_btn)
