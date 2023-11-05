from aiogram import Bot
from aiogram.types import CallbackQuery
from core.utils.callbackdata import MacInfo

#вкладки инлайн клавиатуры
async def select_macbook(call: CallbackQuery, bot: Bot, callback_data: MacInfo):
    model = callback_data.model
    size = callback_data.size
    chip = callback_data.chip
    year = callback_data.year
    answer = f'{call.message.from_user.first_name}, ты выбрал Apple MacBook {model}, с диагональю {size}, на чипе {chip},' \
             f' и год выпуска {year}'
    await call.message.answer(answer)
    await call.answer()
