from aiogram import Dispatcher
from aiogram.types import Message


async def echo_all(message: Message):
    await message.bot.send_message(chat_id=message.chat.id, text="gj[eq")


def register_echo(dp: Dispatcher):
    dp.register_message_handler(echo_all)
