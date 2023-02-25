from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import asyncio
from config import API_TOKEN
from db import Database
import chat_commands

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
)


async def on_startup(_):

    await bot.send_message(1130398207, text='Бот запущен')


async def set_all_default_commands(Bot):
    await set_all_default_commands(Bot)


loop = asyncio.new_event_loop()
bot = Bot(API_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)
db = Database('base.db')


async def shutdown(dp):
    await storage.close()
    await bot.close()


if __name__ == '__main__':
    from handlers import dp, send_hello
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=shutdown,
                                                        skip_updates = True
    )
