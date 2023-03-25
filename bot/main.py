import logging
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import API_TOKEN
from database.db import Database


logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )


async def on_startup(_):
    from chat_handlers.handlers import register_all_handlers
    from commands.chat_commands import set_default_commands
    await register_all_handlers(dp)
    await set_default_commands(bot)
    await bot.send_message(1130398207, text='Бот запущен')


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
bot = Bot(API_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot=bot, loop=loop, storage=storage)
db = Database('database/clients.db')


async def shutdown(dp):
    try:
        await storage.close()
        await bot.close()
    finally:
        db.conn.close()

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup,
                            on_shutdown=shutdown,
                            skip_updates=True
                           )
