from aiogram import Bot
from aiogram.types import Message
from core.keyboard.reply import reply_keyboard, loc_tel_poll_keyboard, get_reply_keyboard
from core.keyboard.inline import select_macbook, get_inline_keyboard
from core.utils.dbconnect import Request

async def get_inline(message: Message, bot: Bot): #инлайн кнопка
    await message.answer(f'Привет, {message.from_user.first_name}. это инлайн кнопки',
                         reply_markup=get_inline_keyboard())

async def get_start(message: Message, bot: Bot, counter: str, request: Request):
    await request.add_data(message.from_user.id, message.from_user.first_name)
    await message.answer(f'Сообщение #{counter}') # Показ сколько сообщений в чате
    # await bot.send_message(message.from_user.id, f'Ку {message.from_user.first_name}. Как ты?') #Сообщение в лс бота
    await message.answer(f'<b>Привет, {message.from_user.first_name}. Чем могу помочь?</b>', # ответ на /start
                         reply_markup=get_reply_keyboard()) #Сообщение в группу
    # await message.reply(f'Ку {message.from_user.first_name}. Как ты?') #Сообщение с отметкой пользователя

async def get_location(message: Message, bot: Bot):
    await message.answer(f'Ты отправил геолокацию' f'{message.location.latitude}{message.location.latitude}') #отправляет геолокацию

async def get_photo(message: Message, bot: Bot):
    await message.answer(f'Картинка отправлена. Сохраняю') #ответ на отправленную картинку
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, 'photo.jpg')


async def get_hello(message: Message, bot: Bot):
    await message.answer(f'И тебе привет, {message.from_user.full_name}' ) #ответ на Привет
