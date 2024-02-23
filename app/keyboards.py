from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

# main_kb = [
#     [KeyboardButton(text='Каталог'),
#      KeyboardButton(text='Корзина')],
#     [KeyboardButton(text='Мой профиль'),
#      KeyboardButton(text='Контакты')],
#     [KeyboardButton(text='Актуальность')],
#     [KeyboardButton(text='Объявления')]
# ]

main_kb = [
    [KeyboardButton(text='Помощь')]
]

main_kb_admin = [
    [KeyboardButton(text='Актуальность')],
    [KeyboardButton(text='Объявления')],
    [KeyboardButton(text='Помощь')]
]

main = ReplyKeyboardMarkup(keyboard=main_kb,
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт ниже')

main_admin = ReplyKeyboardMarkup(keyboard=main_kb_admin,
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт ниже')



socials = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Telegram', url='https://t.me/sudoteach')],
    [InlineKeyboardButton(text='YouTube', url='https://youtube.com/@sudoteach')]
])

catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='adidas', callback_data='adidas')],
    [InlineKeyboardButton(text='Nike', callback_data='nike')]
])

listing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='В работу', callback_data='listing_inwork')],
    [InlineKeyboardButton(text='Написать', callback_data='listing_message')]
])

async def create_keyboard(buttons:list, len_row=2):
    inline_keyboard = []
    row = []
    for button in buttons:
        row.append(InlineKeyboardButton(text=button, callback_data=f"button_{button}"))
        if len(row) == len_row:
            inline_keyboard.append(row)
            row = []
    if row:
        inline_keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)