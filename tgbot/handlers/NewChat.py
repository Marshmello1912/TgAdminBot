from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.DataBases.DataBaseModule import add_new_chat


async def add_chat(message: Message):
    add_new_chat(int(message.chat.id))
    await message.answer(text='Чат добавлен в базу данных')


def register_newChat(dp: Dispatcher):
    dp.register_message_handler(add_chat, commands="New_chat", state=["*"])
