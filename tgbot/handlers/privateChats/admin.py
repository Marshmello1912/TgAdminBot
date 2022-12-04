from aiogram import Dispatcher
from aiogram.types import Message

async def send_bot_message(message: Message):
    if message.chat.type == 'private':
        Message_for_send = ' '.join(map(str, message.text[6:].split()[1:]))
        Chat_Id = int(message.text[6:].split()[0])

        await message.bot.send_message(chat_id=Chat_Id, text=Message_for_send)
        del Message, Chat_Id


async def set_new_chat_title(message: Message):
    if message.chat.type == 'private':
        New_Name = ' '.join(map(str, message.text.split()[2:]))
        Chat_Id = int(message.text.split()[1])

        await message.bot.set_chat_title(Chat_Id, New_Name)
        await message.answer('Имя группы успешно изменено')
        del New_Name, Chat_Id


def register_admin_on_private(dp: Dispatcher):
    dp.register_message_handler(send_bot_message, commands=["send"], is_admin=True)
    dp.register_message_handler(set_new_chat_title, commands=['change_GroupName'], is_admin=True)
