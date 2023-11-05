from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.callbackdata import MacInfo

select_macbook = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Macbook Air 13" M1 2020', #Поменять на свой товар
            callback_data='apple_air_13_m1_2020' #Описание товара
        )
    ],
    [
        InlineKeyboardButton(
            text='Macbook Pro 14" M1 pro 2021',
            callback_data='apple_pro_14_m1_2021'
        )
    ],
    [
        InlineKeyboardButton(
            text='Apple Macbook Pro 16" 2019',
            callback_data='apple_pro_16_2019'
        )
    ],
    [
        InlineKeyboardButton(
            text="Link", #для ссылки
            url="https://www.youtube.com" #сама ссылка
        )
    ],
    [
        InlineKeyboardButton(
            text="Профиль создателя",
            url="" #ставим свою ссылку
        )
    ]
])

def get_inline_keyboard(): #Тоже самое как и вверху
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Macbook Air 13" M1 2020', callback_data=MacInfo(model='air', size='13', chip='m1', year='2020'))
    keyboard_builder.button(text='Macbook Pro 14" M1 pro 2021', callback_data=MacInfo(model='pro', size='14', chip='m1', year='2021'))
    keyboard_builder.button(text='Apple Macbook Pro 16" 2019', callback_data=MacInfo(model='pro', size='16', chip='i7', year='2023'))
    keyboard_builder.button(text="Link", url="https://www.youtube.com")
    keyboard_builder.button(text="Профиль создателя", url="")

    keyboard_builder.adjust(3, 1, 1)
    return keyboard_builder.as_markup()