from aiogram import Bot

async def send_message_time(bot: Bot):
    await bot.send_message(, f'Это сообщение отправлено через несколько секунд после старта') #вводим id своего тг бота

async def send_message_cron(bot: Bot):
    await bot.send_message(, f'Это сообщение отправляется ежедневно')  #вводим id своего тг бота

async def send_message_interval(bot: Bot):
    await bot.send_message(, f'Это сообщение отправляется с интервалом в 1 минуту')  #вводим id своего тг бота


async def send_message_middleware(bot: Bot, chat_id: int):
    await bot.send_message(chat_id, f'Рад знакомству') # отправит после заполнения опроса