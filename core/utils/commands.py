from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
#Стартовые команды
async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description="Начало работы"
        ),
        BotCommand(
            command='help', #настраиваем под себя
            description='Помощь'
        ),
        BotCommand(
            command='cancel', #настраиваем под себя
            description='Сбросить'
        ),
        BotCommand(
            command="inline",
            description="Показать инлайн клавиатуру"
        ),
        BotCommand(
            command="pay",
            description="Оплата"

        ),
        BotCommand(
            command="form",
            description="Начать опрос"
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())