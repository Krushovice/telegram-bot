import os
import json

from main import bot, dp, types, db
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, Document, ReplyKeyboardHide
from aiogram.dispatcher.filters import Text, Command
from aiogram.types.message import ContentType
from config import PAYMENTS_TOKEN, item_url
from info import MESSAGES, STATEMENTS
from chat_bottons.Markups import main_Menu, Keyboard_inline

PRICES = [LabeledPrice(label='Справка', amount=1000000)]


@dp.message_handler(Command('start'))
async def start_menu(message: Message):
    await message.answer(MESSAGES['INFO'])
    if (not db.user_exists(message.from_user.id)):
        await bot.send_message(message.from_user.id,
                               f"Здравствуйте, {message.from_user.first_name}.\nПожалуйста, укажите вашу почту",
                               reply_markup=main_Menu)
    else:
        await message.bot.send_message(message.from_user.id, f'''Здравствуйте,
                                      {message.from_user.first_name}''',
                                       reply_markup=main_Menu
                                       )


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

@dp.message_handler(Text(equals=['@']))
async def process_email(message: types.Message):
    # Проверяем, что сообщение содержит корректный email
    if "@" in message.text:
        email = message.text
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
    else:
        # Сообщаем пользователю об ошибке
        await message.answer("Кажется, это не email. Попробуй еще раз.")


@dp.message_handler(Text(equals=['user_btn', 'help_btn', 'join_btn']))
async def bottons(message: Message):
    await message.answer(message.text, reply_markup=ReplyKeyboardHide())
    await message.delete()


@dp.message_handler(Text(equals=['📕 Помощь', '🆕 Карточка клиента', '💵 Получить услугу']))
async def kb_answers(message: Message):
    if message.text == '📕 Помощь':
        await message.answer(MESSAGES['INFO'])
    elif message.text == '🆕 Карточка клиента':
        await message.answer('Для дальнейших действий введите команду /broker и выберите вашего брокера из списка ')
    elif message.text == '💵 Получить услугу':
        await message.answer('Чтобы получить услугу, пожалуйста введите команду /buy и следуйте дайльнейшим инструкциям')


@dp.message_handler(Command('broker'))
async def broker_choice(message: Message):
    await message.reply('Пожалуйста, выберите вашего брокера из списка', reply_markup=Keyboard_inline)


@dp.callback_query_handler(text=['bks', 'open', 'vtb', 'tnkf', 'alfa', 'freadom', 'finam', 'capital'])
async def broker_value(call: types.CallbackQuery):
    if call.data == 'bks':
        broker = 'БКС Брокер.'
        message = (
            """Вы выбрали БКС Брокер. Так держать!
            Пожалуйста, отправьте выписку с вашего банка,
            а далее воспользуйтесь командой /buy"""
        )
    elif call.data == 'open':
        broker = 'Открытие'
        message = (
            """Вы выбрали Открытие.Так держать!
            Пожалуйста, отправьте выписку с вашего банка,
            а далее воспользуйтесь командой /buy"""
        )
    elif call.data == 'vtb':
        broker = 'ВТБ Капитал Форекс'
        message = (
            """Вы выбрали ВТБ Капитал Форекс.Так держать!
            Пожалуйста, отправьте выписку с вашего банка,
            а далее воспользуйтесь командой /buy"""
        )
    elif call.data == 'tnkf':
        broker = 'Тинькофф Инвестиции'
        message = (
            """Вы выбрали Тинькофф Инвестиции.Так держать!
            Пожалуйста, отправьте выписку с вашего банка,
            а далее воспользуйтесь командой /buy"""
        )
    elif call.data == 'alfa':
        broker = 'Альфа Инвестиции'
        message = (
            """Вы выбрали Альфа Инвестиции.Так держать!
            Пожалуйста, отправьте выписку с вашего банка,
            а далее воспользуйтесь командой /buy"""
        )
    elif call.data == 'freadom':
        broker = 'Фридом Финанс'
        message = (
            """Вы выбрали Фридом Финанс.Так держать!
            Пожалуйста, отправьте выписку с вашего банка,
            а далее воспользуйтесь командой /buy"""
        )
    elif call.data == 'finam':
        broker = 'Финам'
        message = (
            """Вы выбрали Финам.Так держать!
            Пожалуйста, отправьте выписку с вашего банка,
            а далее воспользуйтесь командой /buy"""
        )
    elif call.data == 'capital':
        broker = 'IT Capital'
        message = (
            """Вы выбрали IT Capital.Так держать!
            Пожалуйста, отправьте выписку с вашего банка,
            а далее воспользуйтесь командой /buy"""
        )
    db.insert_broker(call.from_user.id, broker)
    await call.message.answer(message)


STATE_PATH = 'bot/info.py'

# Загружаем словарь с ссылками на файлы из файла info.py, если он существует
if os.path.isfile(STATE_PATH):
    with open(STATE_PATH, 'r') as f:
        STATEMENTS.update(json.load(f))
else:
    STATEMENTS = {}


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def handle_pdf(message: Message):
    if message.document.mime_type == 'application/pdf':
        # Проверяем, что загруженный файл имеет расширение .pdf
        file_id = message.document.file_id
        file_name = message.document.file_name
        if message.document.file_unique_id in STATEMENTS:
            await message.answer("Вы уже загружали этот файл.")
            return
        # Сохраняем файл на диск в директорию /home/krushovice/statements с именем, основанным на полном имени пользователя
        user_full_name = message.from_user.full_name
        file_path = f"/home/krushovice/statements/{user_full_name}_{file_name}"
        await bot.download_file_by_id(file_id, file_path)

        # Добавляем ссылку на файл в словарь и сохраняем словарь в файл info.py
        STATEMENTS[message.from_user.id] = file_path
        with open(STATE_PATH, 'w') as f:
            json.dump(STATEMENTS, f)

        await message.answer("Файл успешно сохранен.")
    else:
        await message.answer("Файл должен быть в формате PDF.")


async def register_all_handlers(dp):
    dp.register_message_handler(start_menu, commands=['start'])
    dp.register_message_handler(buy_process, commands=['buy'])
    dp.register_pre_checkout_query_handler(checkout_process)
    dp.register_message_handler(succesful_payment, content_types=types.ContentType.SUCCESSFUL_PAYMENT)
    dp.register_message_handler(process_email, content_types=types.ContentType.TEXT)
    dp.register_message_handler(bottons, Text(equals=['user_btn', 'help_btn', 'join_btn']))
    dp.register_message_handler(kb_answers, Text(equals=['📕 Помощь', '🆕 Карточка клиента', '💵 Получить услугу']))
    dp.register_message_handler(broker_choice, commands=['broker'])
    dp.register_callback_query_handler(broker_value, text=['bks', 'open', 'vtb', 'tnkf', 'alfa', 'freadom', 'finam', 'capital'])
    dp.register_message_handler(handle_pdf, content_types=types.ContentTypes.DOCUMENT)
