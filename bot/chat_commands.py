from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_default_commands(Bot):

    return await bot.set_my_commands(

        commands = [
            BotCommand('help', 'Помощь'),
            BotCommand('buy', 'Купить справку'),
            BotCommand('register', 'Регистрация пользователя'),

        ],
        scope=BotCommandScopeDefault()
    )
