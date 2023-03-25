import logging
import asyncio

from commands import chat_commands
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import API_TOKEN
from database.db import Database


logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
)


async def on_startup(_):
    from chat_handlers.handlers import register_all_handlers
    await register_all_handlers(dp)
    await bot.send_message(1130398207, text='Бот запущен')


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
bot = Bot(API_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot=bot, loop=loop, storage=storage)
db = Database('database/clients.db')


async def set_all_default_commands(Bot):
    await set_all_default_commands(bot)


async def shutdown(dp):
    await storage.close()
    await bot.close_bot()
    await Database().close()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup,
                            on_shutdown=shutdown,
                            skip_updates=True)
