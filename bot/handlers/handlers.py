from telegram_bot.bot.main import bot, dp, types, db
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, Document
from aiogram.dispatcher.filters import Text, Command
from aiogram.types.message import ContentType
from telegram_bot.bot.config import PAYMENTS_TOKEN, item_url
from telegram_bot.bot.info import MESSAGES, STATEMENTS
from telegram_bot.bot.markups.Markups import main_Menu, Keyboard_inline, ReplyKeyboardRemove

PRICES = [LabeledPrice(label='Справка', amount = 1000000)]


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
    await bot.send_message(message.chat.id, f"""Платеж на сумму 10000 рублей прошел успешно!👏🏻👏🏻👏🏻
В течение 24 часов⌛ на вашу почту придёт готовая справка✅""")


@dp.message_handler(Command('start'))
async def start_menu(message: Message):
    if (not db.user_exists(message.from_user.id)):
        await bot.send_message(message.from_user.id,
                                f'''Здравствуйте, {message.from_user.full_name}.
                                Пожалуйста, укажите вашу почту''',
                                reply_markup=main_Menu)

        await message.bot.send_message(message.from_user.id, f'Здравствуйте, {message.from_user.first_name}',
                                       reply_markup=main_Menu
                                       )


@dp.message_handler(content_types=types.ContentType.TEXT)
async def process_email(message: types.Message):
    # Проверяем, что сообщение содержит корректный email
    if "@" in message.text:
        email = message.text
        db.insert_user(
        message.from_user.id,
        message.from_user.full_name,
        message.from_user.username,
        email,
        broker
        )
        await message.answer("Спасибо! Я сохранил твой email.")
    else:
         # Сообщаем пользователю об ошибке
        await message.answer("Кажется, это не email. Попробуй еще раз.")


@dp.message_handler(Text(equals=['user_btn', 'help_btn', 'join_btn']))
async def bottons(message: Message):
    await message.answer(message.text, reply_markup=ReplyKeyboardRemove())
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


@dp.callback_query_handler(text=['bks', 'open', 'vtb', 'tnkf'])
async def broker_value(call: types.CallbackQuery):
    if call.data == 'bks':
        broker = 'БКС Брокер.'
        await call.message.answer("Вы выбрали БКС Брокер. Так держать!\nПожалуйста, отправьте выписку с вашего банка, а далее воспользуйтесь командой /buy")
    if call.data == 'open':
        broker = 'Открытие'
        await call.message.answer("Вы выбрали Открытие. Так держать!\nПожалуйста, отправьте выписку с вашего банка, а далее воспользуйтесь командой /buy")
    if call.data == 'vtb':
        broker = 'ВТБ Капитал Форекс'
        await call.message.answer("Вы выбрали ВТБ Капитал Форекс.\nПожалуйста, отправьте выписку с вашего банка, а далее воспользуйтесь командой /buy")
    if call.data == 'tnkf':
        broker = 'Тинькофф Инвестиции'
        await call.message.answer("Вы выбрали Тинькофф Инвестиции.\nПожалуйста, отправьте выписку с вашего банка, а далее воспользуйтесь командой /buy")
    if call.data == 'alfa':
        broker = 'Альфа Инвестиции'
        await call.message.answer("Вы выбрали Альфа Инвестиции.\nПожалуйста, отправьте выписку с вашего банка, а далее воспользуйтесь командой /buy")
    if call.data == 'freadom':
        broker = 'Фридом Финанс'
        await call.message.answer("Вы выбрали Фридом Финанс.\nПожалуйста, отправьте выписку с вашего банка, а далее воспользуйтесь командой /buy")
    if call.data == 'finam':
        broker = 'Финам'
        await call.message.answer("Вы выбрали Финам.\nПожалуйста, отправьте выписку с вашего банка, а далее воспользуйтесь командой /buy")
    if call.data == 'capital':
        broker = 'IT Capital'
        await call.message.answer("Вы выбрали IT Capital.\nПожалуйста, отправьте выписку с вашего банка, а далее воспользуйтесь командой /buy")
    db.insert_broker(call.from_user.id, broker)
    await call.answer()


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def handle_pdf(message: Message):
    if message.document.mime_type == 'application/pdf':
        # Проверяем, что загруженный файл имеет расширение .pdf
        file_id = message.document.file_id
        file_unique_id = message.document.file_unique_id
        file_name = message.document.file_name

        # Сохраняем файл на диск с именем, основанным на полном имени пользователя
        user_full_name = message.from_user.full_name
        file_path = f"{user_full_name}_{file_name}"
        await bot.download_file_by_id(file_id, file_path)

        # Добавляем ссылку на файл в словарь и отправляем пользователю сообщение о том, что файл был успешно сохранен
        STATEMENTS[user_full_name] = file_path
        await message.answer("Файл успешно сохранен.")
    else:
        # Если загруженный файл не является pdf, сообщаем пользователю об ошибке
        await message.answer("Файл должен быть в формате PDF.")





# @dp.message_handler()
# async def info_command(message: types.Message):
#     if message.text=='📕Информация':
#         await bot.send_message(message.from_user.id,text=INFO)
#         await message.delete()
#     elif message.text=='🔙Главное меню':
#         await bot.send_message(message.from_user.id,'🔙Главное меню',reply_markup=nav.main_Menu)
#         await message.delete()
#     elif message.text=='🔛Другое':
#         await bot.send_message(message.from_user.id,'🔛Другое',reply_markup=nav.other_Menu)
#         await message.delete()
#     elif message.text=='💵Получить услугу':
#         await bot.send_message(message.from_user.id,'💵Получить услугу')
#         await message.delete()
#     elif message.text=='📩Отправить выписку':
#         await bot.send_message(message.from_user.id,'📩Отправить выписку')
#         await message.delete()

#     else:
#         await message.reply('Неизвестная команда')
