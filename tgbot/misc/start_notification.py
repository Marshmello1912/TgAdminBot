from aiogram import Dispatcher

from tgbot.config import load_config


async def start_notification(dp: Dispatcher):
    admins = load_config().tg_bot.admin_ids
    for admin in admins:
        await dp.bot.send_message(admin, "Bot is start")
