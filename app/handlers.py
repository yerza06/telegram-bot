import os
import logging
from typing import List
from aiogram import F, Router, html, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from rich.logging import RichHandler
from datetime import datetime


from sqliter import SQLiter
from config import CHATID
from config import TOKEN
from app.filters.is_admin import IsAdmin


db = SQLiter("database.db")
bot = Bot(token=TOKEN)
router = Router()
log = logging.getLogger("rich")


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    userId = message.from_user.id
    firstName = message.from_user.first_name
    lastName = message.from_user.last_name
    fullName = message.from_user.full_name
    username = message.from_user.username
    language_code = message.from_user.language_code
    is_premium = message.from_user.is_premium

    directory = f'./users/{userId}-{fullName}-{username}'
    file_path = f'{directory}/chat.md'
    os.makedirs(directory, exist_ok=True)

    try:
        file = open(file_path, 'r', encoding='utf-8')
    except FileNotFoundError:
        file = open(file_path, 'w', encoding='utf-8')
        file.write('---\n')
        file.write(f'User ID: {userId}\n')
        file.write(f'Full Name: {fullName}\n')
        file.write(f'Username: {username}\n')
        file.write(f'Language Code: {language_code}\n')
        file.write(f'Is Premium: {is_premium}\n')
        file.write('---\n')
        file.close()

    pho = await bot.get_user_profile_photos(message.from_user.id)
    if pho.total_count == 0:
        await message.answer("У вас нет фотографии профиля.")
        return
    for i in range(pho.total_count):
        p = pho.photos[i][0].file_id
        info = await bot.get_file(p)
        file_path = info.file_path

        os.makedirs(f'{directory}/profile photos', exist_ok=True)

        await bot.download_file(file_path, f'{directory}/profile photos/{i}.jpg')

    log.info(f"The user Launched the bot @{username} id={userId} - \'{fullName}\'")
    cursor = db.user_exists(userId)
    if cursor == 0:
        db.add_user(userId, firstName, lastName, username, language_code, is_premium)
        log.info(f"The user has been added to the database @{username} id={userId} - \'{fullName}\'")
    elif cursor == 1:
        log.info(f"The user already exists @{username} id={userId} - \'{fullName}\'")
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@router.message(Command("getUsers"), IsAdmin(CHATID))
async def command_get_users(message: Message):
    await message.answer(db.get_users())
        

@router.message(Command("getUserInfo"), IsAdmin(CHATID))
async def command_get_users(message: Message):
    id = message.text[13:]

    try: 
        data = db.get_user_info(id)
        await message.answer(f"\nFull Name: {data[0]} {data[1]}\nUsername: @{data[3]}\nID: {html.code(data[2])}\nDate: {data[4]}\nLanguage: {data[5]}\nIs Premium: {data[6]}")
    except TypeError as er:
        await message.answer(f'{er}')


@router.message()
async def echo_handler(message: Message) -> None:
    userId = message.from_user.id
    fullName = message.from_user.full_name
    username = message.from_user.username
    fullName = message.from_user.full_name
    username = message.from_user.username
    try:
        await message.answer("Ведите команду /start")
        today = datetime.now().today()
        user = open(f'./users/{userId}-{fullName}-{username}/chat.md', 'a', encoding='utf-8')
        user.write(f'{today} => {message.text}\n')
        user.close()
    except TypeError:
        await message.answer("Nice try!")