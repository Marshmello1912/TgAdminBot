from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.config import load_config
from tgbot.services.DataBases.DataBaseModule import mute, unmute, warn, unwarn


# *��� ����������� � ���� �� ������ �� ���������
async def mute_user(message: Message):
    config = load_config(".env")
    muted_user_id = message.reply_to_message.from_user.id
    muted_user_name = message.reply_to_message.from_user.username
    if muted_user_id == message.from_user.id:  # �������� �� ��� ������ ����
        await message.answer('�� �����, ����� ���� ������?')
    elif message.reply_to_message.from_user.is_bot:  # �������� �� ��� ����
        await message.answer('��, �� ��� ������)')
    elif muted_user_id in config.tg_bot.admin_ids:  # �������� �� ��� ������
        await message.answer('��, �� ��� ������, ��� �����)))')
    else:
        Mute = mute(message.chat.id, muted_user_id, muted_user_name)
        if Mute:  # �������� �� ��� ������������ ������������
            await message.bot.restrict_chat_member(message.chat.id, muted_user_id, can_send_messages=False,
                                                   can_send_media_messages=False,
                                                   can_send_other_messages=False, can_add_web_page_previews=False)
            await message.answer(f'@{muted_user_name}, �������')
        else:
            await message.answer(f'@{muted_user_name}, ��� � ���� � �� ����� ������ � ���� ���')
        del config, muted_user_id, muted_user_name


# * ������ ������������ �� ������ �� ���������
# ! �� ������ �������(��������) ������ �� Id ������������
async def unmute_user(message):
    config = load_config(".env")
    unmuted_user_id = message.reply_to_message.from_user.id
    unmuted_user_name = message.reply_to_message.from_user.username

    unmute(message.chat.id, unmuted_user_id, unmuted_user_name)
    if unmuted_user_id in config.tg_bot.admin_ids:  # �������� �� ������
        await message.answer('����� �� ����� ���� � ����)))')
    else:
        await message.bot.restrict_chat_member(message.chat.id, unmuted_user_id, can_send_messages=True,
                                               can_send_media_messages=True,
                                               can_send_other_messages=True, can_add_web_page_previews=True)
        await message.answer(f'@{unmuted_user_name}, �� ��������')


# * ���� ������������ �� ������ �� ���������
async def Warn_User(message: Message):
    config = load_config(".env")
    print(config.tg_bot.admin_ids)
    warnForUser_id = message.reply_to_message.from_user.id
    warnForUser_name = message.reply_to_message.from_user.username
    print(warnForUser_id)
    Warn = warn(message.chat.id, warnForUser_id, warnForUser_name)
    if warnForUser_id == message.from_user.id:  # �������� �� ���� ������ ����
        await message.answer('�� �����, ����� ���� �������?')
    elif message.reply_to_message.from_user.is_bot:  # �������� �� ���� ����
        await message.answer('��, �� ��� ������)')
    elif warnForUser_id in config.tg_bot.admin_ids:  # �������� �� ���� ������
        await message.answer('��, �� ��� ������, ��� �����)))')
    else:
        if Warn == -1:
            await mute_user(message)
            await message.answer(f'@{warnForUser_name} �� �������(�) 3 �������������� � ������ �� '
                                 f'������ '
                                 f'������ � ���� ��� ')
        else:
            await message.answer(f'@{warnForUser_name} � ���� {Warn} ��������������')
    del Warn, warnForUser_id, warnForUser_name, config


# * ������ ���� ������ � ������������ �� ������ �� ��������� (�� ���������)
async def unWarn_User(message: Message):
    config = load_config(".env")
    unwarnForUser_id = message.reply_to_message.from_user.id
    unwarnForUser_name = message.reply_to_message.from_user.username
    unwarn(message.chat.id, unwarnForUser_id, unwarnForUser_name)
    if unwarnForUser_id in config.tg_bot.admin_ids:  # �������� �� ������
        await message.answer('� ������ �� ����� ���� warn\'��)))')
    else:
        await message.answer(f'@{unwarnForUser_name} ��� ������������� � ���� �����) ')


def register_admin(dp: Dispatcher):
    dp.register_message_handler(Warn_User, commands="warn", state="*", is_admin=True)
    dp.register_message_handler(unWarn_User, commands="unwarn", state="*", is_admin=True)

    dp.register_message_handler(mute_user, commands="mute", state="*", is_admin=True)
    dp.register_message_handler(mute_user, commands="unmute", state="*", is_admin=True)
