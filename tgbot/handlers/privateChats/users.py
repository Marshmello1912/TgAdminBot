from aiogram import Dispatcher
from aiogram.types import Message


async def send_user_id(message: Message):
    if message.chat.type == 'private':
        await message.answer(message.from_user.id)


def register_users_on_private(dp: Dispatcher):
    dp.register_message_handler(send_user_id, state=["*"])
