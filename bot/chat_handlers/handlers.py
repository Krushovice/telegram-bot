import os
import json
import re

from typing import match
from aiogram import types
from main import bot, dp, db
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, Document
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.message import ContentType
from config import PAYMENTS_TOKEN, item_url
from info import MESSAGES
from chat_bottons.Markups import main_Menu, Keyboard_inline

PRICES = [LabeledPrice(label='Справка', amount=1000000)]


# class UserState(StatesGroup):
#     email = State()
#     broker = State()


@dp.message_handler(Command('start'))
async def start_menu(message: Message):
    await message.answer(MESSAGES['Hello'])
    if (not db.user_exists(message.from_user.id)):
        await bot.send_message(message.from_user.id,
                               f"Здравствуйте, {message.from_user.first_name}.Пожалуйста, укажите вашу почту",
                               reply_markup=main_Menu
                               )
    else:
        await message.bot.send_message(message.from_user.id, f'Здравствуйте, {message.from_user.first_name}!',
                                       reply_markup=main_Menu
                                       )


@dp.message_handler(Command('help'))
async def help_user(message: Message):
    await message.answer(MESSAGES['Help'])


@dp.message_handler(Command('buy'))
async def buy_process(message: Message):
    await bot.send_invoice(message.chat.id,
                          title=MESSAGES['tm_title'],
                          description=MESSAGES['tm_description'],
                          provider_token=PAYMENTS_TOKEN,
                          currency='rub',
                          photo_url=item_url,
                          photo_height=512,
                          photo_width=512,
                          photo_size=512,
                          need_email=True,
                          need_phone_number=True,
                          is_flexible=False,
                          prices=PRICES,
                          start_parameter='example',
                          payload='some_invoice'
                           )


@dp.message_handler(Command('register'))
async def check_user(message: Message):
    if db.user_exists(message.from_user.id):
        await message.answer('Вы уже зарегистрированы в базе данных!\n'
                             'Пожалуйста, отправьте справку в формате .pdf\n'
                             'а затем оплатите услугу по команде /buy'
                             )
    else:
        await message.answer('Для того, чтобы зарегистрироваться,\n'
                             'необходимо отправить в чат свою почту,\n'
                             'а затем выбрать брокера /broker'
                             )


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def succesful_payment(message: Message):
    if message.successful_payment.total_amount == 1000000:
        await bot.send_message(message.chat.id,
                               """Платеж на сумму 10000 рублей прошел успешно!👏🏻👏🏻👏🏻
                               В течение 24 часов⌛ на вашу почту придёт готовая справка✅""")
    else:
        await bot.send_message(message.chat_id,
                               """Неверная сумма платежа,
                               повторите попытку!""")


@dp.message_handler(Text(equals=['user_btn', 'help_btn', 'join_btn']))
async def bottons(message: Message):
    await message.answer(message.text)
    await message.delete()


@dp.message_handler(Text(equals=['📕 Помощь', '🆕 Карточка клиента', '💵 Получить услугу', '@']))
async def kb_answers(message: Message):

    if "@" in message.text:
        email = message.text
        # Проверяем, что введенная строка является корректным email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            await message.answer("Некорректный email. Пожалуйста, введите корректный email.")
            return

        user_id = message.from_user.id
        if db.user_exists(user_id):
            # Если пользователь уже существует, обновляем его email
            db.update_user_email(user_id, email)
            await message.answer("Твой email успешно обновлен.")
        else:
            # Если пользователь не существует, добавляем его в базу данных
            db.insert_user(
                user_id,
                message.from_user.full_name,
                message.from_user.username,
                email,
                broker=None
            )
            await message.answer("Спасибо! Я сохранил твой email.")

    elif message.text == '📕 Помощь':
        await message.answer(MESSAGES['Help'])

    elif message.text == '🆕 Карточка клиента':
        await message.answer('Для дальнейших действий введите команду /broker и выберите вашего брокера из списка ')

    elif message.text == '💵 Получить услугу':
        await message.answer('Чтобы получить услугу, пожалуйста введите команду /buy и следуйте дайльнейшим инструкциям')


@dp.message_handler(Command('broker'))
async def broker_choice(message: Message):
    await message.reply('Пожалуйста, выберите вашего брокера из списка', reply_markup=Keyboard_inline)


@dp.callback_query_handler(text=['bks', 'open', 'vtb', 'tnkf', 'alfa', 'freedom', 'finam', 'capital'])
async def broker_value(call: types.CallbackQuery):
    match call.data:
        case 'bks':
            broker = 'БКС Брокер'

        case 'open':
            broker = 'Открытие'

        case 'vtb':
            broker = 'ВТБ Капитал Форекс'

        case 'tnkf':
            broker = 'Тинькофф Инвестиции'

        case 'alfa':
            broker = 'Альфа Инвестиции'

        case 'freedom':
            broker = 'Фридом Финанс'

        case 'finam':
            broker = 'Финам'

        case 'capital':
            broker = 'IT Capital'

    message = (
        f"Вы выбрали {broker}. Так держать!\n"
        "Пожалуйста, отправьте выписку с вашего банка в формате .pdf,\n"
        "а далее воспользуйтесь командой /buy"
    )
    db.insert_broker(call.from_user.id, broker)
    await call.message.answer(message)


USERS_STATEMENTS_PATH = 'users_statements.json'
if os.path.isfile(USERS_STATEMENTS_PATH):
    with open(USERS_STATEMENTS_PATH, 'r') as f:
        USERS_STATEMENTS = json.load(f)
else:
    USERS_STATEMENTS = {}


# Обработчик для загрузки файлов
@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def handle_pdf(message: Message):
    if message.document.mime_type == 'application/pdf':
        # Проверяем, что загруженный файл имеет расширение .pdf
        file_id = message.document.file_id
        file_name = message.document.file_name
        user_fullname = message.from_user.get.full_name
        user_id = message.from_user.id

        # Получаем словарь с информацией о пользователе и его файлов, если он существует, иначе создаем пустой словарь
        user_info = USERS_STATEMENTS.get(user_id, {'fullname': user_fullname, 'files': {}})

        # Проверяем, что пользователь не загружал ранее этот файл
        if file_name in user_info['files']:
            await message.answer("Вы уже загружали этот файл.")
            return

        # Создаем директорию для пользователя, если она не существует
        user_dir = f"/home/krushovice/statements/{user_fullname}({user_id})"
        os.makedirs(user_dir, exist_ok=True)

        # Сохраняем файл на диск в директорию пользователя с именем, основанным на имени файла
        file_path = os.path.join(user_dir, file_name)
        await bot.download_file_by_id(file_id, file_path)

        # Обновляем словарь с информацией о пользователе и его файлов и сохраняем его в файл
        user_info['files'][file_name] = file_path
        USERS_STATEMENTS[user_id] = user_info
        with open(USERS_STATEMENTS_PATH, 'w') as f:
            json.dump(USERS_STATEMENTS, f)

        await message.answer("Файл успешно сохранен.")

    else:
        await message.answer("Файл должен быть в формате PDF.")


async def register_all_handlers(dp):
    dp.register_message_handler(start_menu, commands=['start'])
    dp.register_message_handler(buy_process, commands=['buy'])
    dp.register_message_handler(help_user, commands=['help'])
    dp.register_message_handler(check_user, commands=['register'])
    dp.register_pre_checkout_query_handler(checkout_process)
    dp.register_message_handler(succesful_payment, content_types=types.ContentType.SUCCESSFUL_PAYMENT)
    dp.register_message_handler(bottons, Text(equals=['user_btn', 'help_btn', 'join_btn']))
    dp.register_message_handler(kb_answers, Text(equals=['📕 Помощь', '🆕 Карточка клиента', '💵 Получить услугу']))
    dp.register_message_handler(broker_choice, commands=['broker'])
    dp.register_callback_query_handler(broker_value, text=['bks', 'open', 'vtb', 'tnkf', 'alfa', 'freadom', 'finam', 'capital'])
    dp.register_message_handler(handle_pdf, content_types=types.ContentTypes.DOCUMENT)
