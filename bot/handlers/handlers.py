from telegram_bot.bot.main import bot, dp, types, db
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.dispatcher.filters import Text, Command
from aiogram.types.message import ContentType
from telegram_bot.bot.config import admin_id, API_TOKEN, PAYMENTS_TOKEN, item_url
from telegram_bot.bot.info import MESSAGES
from telegram_bot.bot.markups.Markups import main_Menu, Keyboard_inline, ReplyKeyboardRemove

PRICES = [LabeledPrice(label='Справка', amount = 1000000)]


async def send_hello(dp):
    await bot.send_message(chat_id=admin_id, text = 'Бот запущен')


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
                          start_parameter = 'example',
                          payload = 'some_invoice')


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
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, f"Здравствуйте, {username} ! Пожалуйста, укажите вашу почту", reply_markup=main_Menu)
    await message.bot.send_message(message.from_user.id, MESSAGES['HELLO'], reply_markup=main_Menu)


@dp.message_handler(Text(equals=['user_btn', 'help_btn', 'join_btn']))
async def bottons(message: Message):
    await message.answer(message.text, reply_markup=ReplyKeyboardRemove())
    await message.delete()


@dp.message_handler(Text(equals=['📕 Помощь', '🆕 Карточка клиента', '💵 Получить услугу']))
async def kb_answers(message: Message):
    if message.text == '📕 Помощь':
        await message.answer(MESSAGES['INFO'])
    elif message.text == '🆕 Карточка клиента':
        await message.answer('Для дальнейших действий,укажите пожалуйста вашу электронную почту, а также введите команду /broker и выберите вашего брокера из списка ')
    elif message.text == '💵 Получить услугу':
        await message.answer('Чтобы получить услугу, пожалуйста введите команду /buy и следуйте дайльнейшим инструкциям')


@dp.message_handler(Text(equals=['@']))
async def mail(message: Message):
    await message.answer(message.text, text='Почта успешна добавлена!')
    await message.delete()


    # @dp.message_handler(Command('file'))
    # async def get_file(message: Message):
    #     await message.answer('Отлично, вы отправили выписку с вашего банка. Пожалуйста, воспользуйтесь меню команд чтобы произвести оплату')
    #     file = await dp.get_file(message.document.file_id)
    #     await dp.download_file(file.file_path,'D:\PythonProjects\Telegram bots\Docs\file_1.pdf')


@dp.message_handler(Command('broker'))
async def broker_choice(message: Message):
    await message.reply('Пожалуйста, выберите вашего брокера из списка', reply_markup=Keyboard_inline)


@dp.callback_query_handler(text=['bks', 'open', 'vtb', 'tnkf'])
async def broker_value(call: types.CallbackQuery):
    if call.data == 'bks':
        await call.message.answer("Вы выбрали БКС Брокер. Так держать!\nОсталось отправить в чат выписку из банка в формате pdf и\nпроизвести оплату по команде /buy ")
    if call.data == 'open':
        await call.message.answer("Вы выбрали Открытие. Так держать!\nОсталось отправить в чат выписку из банка в формате pdf и\nпроизвести оплату по команде /buy ")
    if call.data == 'vtb':
        await call.message.answer("Вы выбрали ВТБ Капитал Форекс. Так держать!\nОсталось отправить в чат выписку из банка в формате pdf и\nпроизвести оплату по команде /buy ")
    if call.data == 'tnkf':
        await call.message.answer("Вы выбрали Тинькофф Инвестиции. Так держать!\nОсталось отправить в чат выписку из банка в формате pdf и\nпроизвести оплату по команде /buy ")
    if call.data == 'alfa':
        await call.message.answer("Вы выбрали Альфа Инвестиции. Так держать!\nОсталось отправить в чат выписку из банка в формате pdf и\nпроизвести оплату по команде /buy ")
    if call.data == 'freadom':
        await call.message.answer("Вы выбрали Фридом Финанс. Так держать!\nОсталось отправить в чат выписку из банка в формате pdf и\nпроизвести оплату по команде /buy ")
    if call.data == 'finam':
        await call.message.answer("Вы выбрали Финам. Так держать!\nОсталось отправить в чат выписку из банка в формате pdf и\nпроизвести оплату по команде /buy ")
    if call.data == 'capital':
        await call.message.answer("Вы выбрали IT Capital. Так держать!\nОсталось отправить в чат выписку из банка в формате pdf и\nпроизвести оплату по команде /buy ")
    await call.answer()




# @dp.message_handler(commands =['start'])
# async def start(message: types.Message):
#     if(not db.user_exists(message.from_user.id)):
#         db.add_user(message.from_user.id)
#         await bot.send_message(message.from_user.id, text = HELLO)
#     else:
#         await bot.send_message(message.from_user.id,'Вы уже зарегистрированы!', reply_markup=nav.main_Menu)

# @dp.message_handler()
# async def bot_message(message: types.Message):
#     if message.chat.type == 'privite':
#         if message.text == '🆕 Карточка клиента':
#            user_nickname = "Ваш ник " + db.get_nickname(message.from_user.id)
#            await bot.send_message(message.from_user.id, user_nickname)

#         else:
#             if db.get_signup(message.from_user.id)== "setnickname":
#                 if(len(message.text) >15):
#                     await bot.send_message(message.from_user.id,'Никнейм не должен превышать 15 символов')
#                 elif '@' in message.text or '/' in message.text:
#                     await bot.send_message(message.from_user.id,'Никнейм содержит запрещенный символ')
#                 else:
#                     db.set_nickname(message.from_user.id,message.text)
#                     db.set_signup(message.from_user.id, 'done')
#                     await bot.send_message(message.from_user.id,'Вы успешно зарегистрированы!', reply_markup=nav.main_Menu)
#             else:
#                 await bot.send_message(message.from_user.id, 'Я вас не понимаю')
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
