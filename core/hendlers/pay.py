from aiogram import Bot
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, InlineKeyboardButton, InlineKeyboardMarkup,\
    ShippingOption, ShippingQuery
#кнопка оплаты


keyboards = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Оплатить",
            pay=True
        )
    ],
    [
        InlineKeyboardButton(
            text='Link',
            url="https://www.twitch.tv/" #ставим свою ссылку
        )
    ]
])


BY_SHIPPING = ShippingOption(
    id='by',
    title='Доставка в Минск',
    prices=[
        LabeledPrice(
            label='Доставка почтой Беларуссии',
            amount=500
        )
    ]
)

RU_SHIPPING = ShippingOption(
    id='ru',
    title='Доставка в Россию',
    prices=[
        LabeledPrice(
            label='Доставка почтой России',
            amount=600

        )
    ]
)

UA_SHIPPING = ShippingOption(
    id='ua',
    title='Доставка в Украину',
    prices=[
        LabeledPrice(
            label="Доставка почтой Украины",
            amount=700
        )
    ]
)


CITIES_SHIPPING = ShippingOption(
    id="capitals",
    title='Быстрая доставка по городу',
    prices=[
        LabeledPrice(
            label="Доставка курьером",
            amount=500
        )
    ]
)

async def shipping_check(shipping_query: ShippingQuery, bot: Bot):
    shipping_options = []
    countries = ['BY', 'RU', 'UA']
    if shipping_query.shipping_address.country_code not in countries:
        return await bot.answer_shipping_query(shipping_query.id, ok=False,
                                               error_message="В вашу страну нет доставки")

    if shipping_query.shipping_address.country_code == 'BY':
        shipping_options.append(BY_SHIPPING)

    if shipping_query.shipping_address.country_code == 'RU':
        shipping_options.append(RU_SHIPPING)

    if shipping_query.shipping_address.country_code == 'UA':
        shipping_options.append(UA_SHIPPING)

    cities = ['Минск', 'Москва', 'Киев']
    if shipping_query.shipping_address.city in cities:
        shipping_options.append(CITIES_SHIPPING)

    await bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options)



async def order(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Покупка через telegram",
        description="Принимаем платежи",
        payload="Сбор статистики",
        provider_token="", #Токен из БотФазер там выбираем терминал
        currency="rub",
        prices=[
            LabeledPrice(
                label="название и цена",
                amount=99000,
            ),
            LabeledPrice(
                label="ндс",
                amount=2000
            ),
            LabeledPrice(
                label="Скидка",
                amount=-2000
            ),
            LabeledPrice(
                label="Бонус",
                amount=-4000
            )
        ],
        max_tip_amount=500, #чаевые
        suggested_tip_amounts=[100, 200, 300, 400], # максимум 4 элемента, сумма чаевых
        start_parameter="qwerty", #обязатально к заполнению
        provider_data=None,
        photo_url="https://ltdfoto.ru/image/yo3xkr", #ссылка на картинку, которая будет в счете
        photo_size=100, #размер картинки
        photo_width=600, #ширина картинки
        photo_height=450, #высота картинки
        need_name=True, #полное имя пользователя(если нужно)
        need_phone_number=True, #Если нужен номер телефона пользователя
        need_email=True, #Если нужен эмейл
        need_shipping_address=True, #Если нужен адрес доставки
        send_phone_number_to_provider=True, #Если просят отправить номер покупателя
        send_email_to_provider=True, #Отправка эмейла
        is_flexible=True, #Если цена зависит от доставки
        disable_notification=False, #Сообщение без звука
        protect_content=False, #Защита от перессылки и копирования
        reply_to_message_id=None, #Отправка в счет пользователя сообщения, то надо будет указать id вместо None
        allow_sending_without_reply=True, #Отправить счет на оплату, если сообщение не найдено
        reply_markup=keyboards, #Если сделать еще клавиатуру, то передать вместо None параметр(Первая кнопка Оплатить)
        request_timeout=15, #Время запроса после счета
    )

async def pre_checkout_query(pre_checkout_query:PreCheckoutQuery, bot:Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def successful_payment(message: Message):
    msg = f'Спасибо за оплату{message.successful_payment.total_amount // 100}{message.successful_payment.currency}.' \
          f'\r\n мы получили заявку.'
    await message.answer(msg)

