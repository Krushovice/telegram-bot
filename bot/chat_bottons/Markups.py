from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

Keyboard_inline = InlineKeyboardMarkup(row_width=3)
Keyboard_inline.add(
    InlineKeyboardButton('📉 БКС Брокер', callback_data='bks'),
    InlineKeyboardButton('🧾 Открытие', callback_data='open'),
    InlineKeyboardButton('📈 ВТБ Капитал Форекс', callback_data='vtb'),
    InlineKeyboardButton('📒 Тинькофф Инвестиции', callback_data='tnkf'),
    InlineKeyboardButton('📕 Альфа Инвестиции', callback_data='alfa'),
    InlineKeyboardButton('📋 Финам', callback_data='finam'),
    InlineKeyboardButton('💹 Фридом Финанс', callback_data='freadom'),
    InlineKeyboardButton('📰 IT Capital', callback_data='capital')
)
# ----Main_menu----

user_btn = KeyboardButton('🆕 Карточка клиента')
help_btn = KeyboardButton('📕 Помощь')
join_btn = KeyboardButton('💵 Получить услугу')
main_Menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(user_btn, help_btn).row(join_btn)
