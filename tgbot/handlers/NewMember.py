from aiogram import Dispatcher
from aiogram.types import Message, ContentTypes

from tgbot.services.DataBases.DataBaseModule import add_new_user


# !cделать так что бы бот не реагировал на добавление cамого cебя в чат
async def welcome_new_member(message: Message):
    if message.new_chat_members[0].is_bot:  # Проверка на бота
        await message.answer(text='Привет брат)')
    else:
        print(message.new_chat_members[-1].username)
        await message.answer(text=f'Привет {message.new_chat_members[-1].first_name}')
        add_new_user(message.chat.id, message.new_chat_members[-1].id, message.new_chat_members[-1].username)


def register_new_user(dp: Dispatcher):
    dp.register_message_handler(welcome_new_member, content_types=ContentTypes.NEW_CHAT_MEMBERS)
