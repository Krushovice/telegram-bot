import logging
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.webhook import SendMessage
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import API_TOKEN, WEBHOOK_URL_PATH, WEBAPP_HOST, WEBAPP_PORT, SSL_CERT, SSL_PRIV_KEY
from database.db import Database

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(token=API_TOKEN, loop=loop, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, loop=loop)
db = Database('database/clients.db')


async def startup(_):
    await bot.set_webhook(WEBHOOK_URL_PATH)
    await bot.send_message(1130398207, text='Бот запущен')


async def shutdown(_):
    try:
        await bot.delete_webhook()
        await storage.close()
        await storage.wait_closed()
        await db.conn.close()
    finally:
        await bot.session.close()


async def webhook(request):
    if request.match_info.get('token') == API_TOKEN:
        update = types.Update.parse_raw(await request.read(), bot)
        await dp.process_update([update])
        return SendMessage(200, "ok")
    return web.Response(status=403)


if __name__ == '__main__':
    # executor.start_polling(dp, on_startup=startup,
    #                        on_shutdown=shutdown,
    #                        skip_updates=True
    #                        )
    token = API_TOKEN
    app = web.Application()
    app.router.add_post(f'/{token}', webhook)
    bot.set_webhook(WEBHOOK_URL_PATH)
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_URL_PATH,
        skip_updates=True,
        on_startup=startup,
        on_shutdown=shutdown,
        app=app,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )
