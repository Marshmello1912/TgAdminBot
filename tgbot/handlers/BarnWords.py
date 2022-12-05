from aiogram import Dispatcher
from aiogram.types import Message


async def BanWords(message: Message):
    banWords = open('tgbot/misc/BannedWords.ini', 'r')
    mes = message.text.lower()
    print(mes)
    for word in banWords.read().split(', '):
        if word in mes:
            await message.answer("банворд")
    banWords.close()


def register_ban_words(dp: Dispatcher):
    dp.register_message_handler(BanWords, state="*")
