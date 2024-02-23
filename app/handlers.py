from aiogram import Router, types, F
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb
import app.data_base as db
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold, bold
from aiogram.filters import Filter
from create_bot import bot, ADMINS, CHAT_ID


router = Router()
TEXT_COMMAND = """
<b>/admin</b> - <em>режим админа</em>
<b>/post</b> - <em>отправить заявки в группу</em>
"""

class Admin(Filter):
    async def __call__(self, message: Message) -> bool:
        return str(message.from_user.id) in ADMINS

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    keyboard = kb.main_admin if str(message.from_user.id) in ADMINS else kb.main 
    await message.answer(f"Приветствую, {hbold(message.from_user.full_name)}!\n\nСписок команд:{TEXT_COMMAND}", reply_markup=keyboard)

@router.message(F.text == '/admin')
async def cmd_admin(message: Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer(f"Режим админа", reply_markup=kb.main_admin)
    else:
        await message.answer(f"У вас нет прав администрирования", reply_markup=kb.main)

@router.message(F.text == 'Помощь')
async def cmd_help(message: types.Message):
    await message.answer(TEXT_COMMAND)

@router.message(Admin(), F.text == 'Актуальность')
async def cmd_actuality(message: Message):
    text = f"проект \"индивидуальный заказчик\" 👉 sarahr.ru\n\n"
    text += f"{hbold('АКТУАЛЬНО!!!')}\n\n"
    marker = '✔️'
    records = await db.get_listings()
    for row in records:
        atr = await db.get_listing_attribute(row[0])
        try:
            text += f"{marker}{hbold(row[1])} №{atr['number']} {atr['city']} {hbold(atr['reward'])} руб.\n"
        except:
            print(row[0])
    await bot.send_message(chat_id=CHAT_ID, text=text)
    # await message.delete()

@router.message(Admin(), F.text == 'Объявления')
async def cmd_listings(message: Message):
    text = f"Опубликовать заявку /post 44016,41660,47474\n\n"
    marker = '✔️'
    records = await db.get_limit_listings(5)
    buttons_list = []
    for row in records:
        atr = await db.get_listing_attribute(row[0])
        try:
            text += f"{marker}{hbold(row[1])} {atr['city']} №{atr['number']}\n"
            buttons_list.append(atr['number'])
        except:
            print(row[0])
    keyboard = await kb.create_keyboard(buttons_list)
    await message.answer(text, reply_markup=keyboard)
    
@router.message(Admin(), F.text.startswith('/post'))
async def cmd_post(message: Message):
    text = message.text.replace('/post','').replace(' ','')
    numbers = text.split(',')
    for number in numbers:
        if number == '':
            continue
        records = await db.get_listing_by_number(number)
        for row in records:
            atr = await db.get_listing_attribute(row[0])
            text = f"{hbold(row[1])}\n"
            text += f"№: {atr['number']}\n"
            text += f"Зарплата: {atr['zp']}\n"
            text += f"Город: {atr['city']}\n\n"
            text += f"{row[2]}\n\n"
            text += f"⚡️Вознаграждение за сотрудника: {hbold(atr['reward'])}₽\n"
            text += f"Оплата: {atr['payment_type']}\n"
            text += f"Гарантийный период: {atr['guarantee']}"
            await bot.send_message(chat_id=CHAT_ID, text=text)

@router.callback_query(Admin(),F.data.startswith('button_'))
async def post_listing(callback: CallbackQuery):
    number = callback.data.replace('button_','')
    records = await db.get_listing_by_number(number)
    for row in records:
        atr = await db.get_listing_attribute(row[0])
        text = f"{hbold(row[1])}\n"
        text += f"№: {atr['number']}\n"
        text += f"Зарплата: {atr['zp']}\n"
        text += f"Город: {atr['city']}\n\n"
        text += f"{row[2]}\n\n"
        text += f"⚡️Вознаграждение за сотрудника: {hbold(atr['reward'])}₽\n"
        text += f"Оплата: {atr['payment_type']}\n"
        text += f"Гарантийный период: {atr['guarantee']}"
        messages = split_message(text)
        for message in messages:
            await bot.send_message(chat_id=CHAT_ID, text=message)
        await callback.answer('')

def split_message(message):
    max_length = 4096
    if len(message) <= max_length:
        return [message]
    else:
        return [message[i:i+max_length] for i in range(0, len(message), max_length)]

@router.message(F.text == '/my_id')
async def cmd_my_id(message: types.Message):
    await message.answer(f"Ваш ID: {message.from_user.id}")
    # await message.reply(f"Ваше имя: {hbold(message.from_user.full_name)}")
    # await message.answer_photo(photo='https://sarahr.ru/wp-content/uploads/2023/09/Home-picture.png', caption='Пример caption')

@router.message(F.text == '/chat_id')
async def cmd_my_id(message: types.Message):
    await message.answer(f"Чат ID: {message.chat.id}")

@router.message()
async def echo_handler(message: types.Message) -> None:
    pass
    #try:
        #await message.send_copy(chat_id=message.chat.id)
    #except TypeError:
        #await message.answer("Nice try!")