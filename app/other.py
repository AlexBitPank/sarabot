from aiogram import Router, types, F
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb
import app.data_base as db
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold, bold
from aiogram.filters import Filter
from create_bot import bot, CHAT_ID

router = Router()

@router.message(F.text == 'Объявление')
async def cmd_listing(message: Message):
    records = await db.get_listings()
    n = 0
    for row in records:
        n += 1
        atr = await db.get_listing_attribute(row[0])
        text = f"{hbold(row[1])}\n"
        text += f"№: {atr['number']}\n"
        text += f"Зарплата: {atr['zp']}\n"
        text += f"Город: {atr['city']}\n\n"
        text += f"{row[2]}\n\n"
        text += f"⚡️Вознаграждение за сотрудника: {hbold(atr['reward'])}₽\n"
        text += f"Оплата: {atr['payment_type']}\n"
        text += f"Гарантийный период: {atr['guarantee']}"
        # await message.answer(text)
        await bot.send_message(chat_id=CHAT_ID, text=text)
        if n == 1:
            break
    await message.delete()

@router.message(F.text == 'Контакты')
async def contacts(message: Message):
    await message.answer('Наши контакты:', reply_markup=kb.socials)

@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите бренд', reply_markup=kb.catalog)

@router.callback_query(F.data == 'adidas')
async def cb_adidas(callback: CallbackQuery):
    await callback.answer('Вы выбрали бренд', show_alert=True)
    await callback.message.answer(f'Вы выбрали {callback.data}')
    # await bot.send_message(chat_id='639266900', text=text)


@router.message(F.text == '/my_id')
async def cmd_my_id(message: types.Message):
    await message.answer(f"Ваш ID: {message.from_user.id}")
    # await message.reply(f"Ваше имя: {hbold(message.from_user.full_name)}")
    # await message.answer_photo(photo='https://sarahr.ru/wp-content/uploads/2023/09/Home-picture.png', caption='Пример caption')

@router.message(F.text == '/chat_id')
async def cmd_my_id(message: types.Message):
    await message.answer(f"Чат ID: {message.chat.id}")

# Пример отправки картинок
@router.message(F.text == '/send_image')
async def cmd_send_image(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAIB4mUVXvKmkZri_Mp-3xN_SkjNh7JVAAJCzTEb-7qwSMBJzwvjQ1GkAQADAgADbQADMAQ',
                               caption='описание')

# Пример обработки фотографий
@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(message.photo[-1].file_id)

# Пример отправки документов
@router.message(F.text == '/send_doc')
async def cmd_send_doc(message: Message):
    await message.answer_document(document='id',
                                  caption='описание')
# Пример обработки документов
@router.message(F.document)
async def get_document(message: Message):
    await message.answer(message.document.file_id)