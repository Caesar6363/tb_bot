import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentType
from core.hendlers.basic import get_start, get_photo, get_hello
import asyncio
import logging
from core.settings import settings
from aiogram.filters import Command, CommandStart
from aiogram import F
from core.utils.commands import set_commands
from core.hendlers.basic import get_location
from core.hendlers.basic import get_inline
from core.hendlers.callback import select_macbook
from core.utils.callbackdata import MacInfo
from core.hendlers.pay import order, pre_checkout_query, successful_payment, shipping_check
from core.middlewares.countermiddleware import CounterMiddleware
from core.middlewares.officehours import OfficeHoursMiddleware
from core.middlewares.dbmiddleware import DbSession
from core.middlewares.apschedulermiddleware import SchedulerMiddleware
import asyncpg
from core.hendlers import form
from core.utils.statesform import StepsForm
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.hendlers import apsched
from datetime import datetime, timedelta

#asyncpg версия 0.28.0
#aiogram версия 3.1.1
#python 3.10.5
#pgAdmin4 PostgreSQL 16

async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен') #запуск бота. Надпись в чат


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот выключен') #выключение бота. Надпись в чат



async def create_pool():
    return await asyncpg.create_pool(user='postgres', password='', database='users',
                                     host='', port='', command_timeout=60) #вводим свой пароль от pgAdmin, хост и порт

async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] -  %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )

    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    poll_connect = await create_pool()
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(apsched.send_message_time, trigger='date', run_date=datetime.now() + timedelta(seconds=10),
                      kwargs={'bot': bot})
    scheduler.add_job(apsched.send_message_cron, trigger='cron', hour=datetime.now().hour,
                      minute= datetime.now().minute + 1, start_date= datetime.now(), kwargs={'bot': bot})
    scheduler.add_job(apsched.send_message_interval, trigger= 'interval', seconds=60, kwargs={'bot': bot})
    scheduler.start()

    dp.update.middleware.register(DbSession(poll_connect))
    dp.message.middleware.register(CounterMiddleware())
    dp.message.middleware.register(OfficeHoursMiddleware())
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    dp.startup.register(start_bot) #запуск бота. Надпись в чат
    dp.shutdown.register(stop_bot) #выключение бота. Надпись в чат
    dp.message.register(form.get_form, Command(commands='form')) #/form
    dp.message.register(form.get_name, StepsForm.GET_NAME) #Опрос имени
    dp.message.register(form.get_last_name, StepsForm.GET_LAST_NAME) # Опрос Фамилии
    dp.message.register(form.get_age, StepsForm.GET_AGE) #Опрос возраста
    dp.message.register(order, Command(commands='pay')) #оплата
    dp.pre_checkout_query.register(pre_checkout_query)
    dp.message.register(successful_payment, F.location(content_types=[ContentType.SUCCESSFUL_PAYMENT]))
    dp.shipping_query.register(shipping_check)
    dp.message.register(get_inline, Command(commands='inline'))
    dp.callback_query.register(select_macbook, MacInfo.filter())
    dp.message.register(get_location, F.location(content_types=[ContentType.LOCATION])) #F.location заменяет ContentTypesFilter
    dp.message.register(get_hello, F.text.lower() == "привет" ) # Ответ бота на привет
    dp.message.register(get_photo, F.photo) # Сохранение картинки
    dp.message.register(get_start, Command(commands=['start', 'run'])) #Запуск для Сохранения картинки
    # dp.message.register(get_start, CommandStart)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())