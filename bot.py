import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.NewMember import register_new_user
from tgbot.handlers.NewChat import register_newChat
from tgbot.handlers.privateChats.admin import register_admin_on_private
from tgbot.handlers.admin import register_admin
from tgbot.handlers.user import register_user
from tgbot.handlers.BarnWords import register_ban_words

from tgbot.middlewares.environment import EnvironmentMiddleware

from tgbot.misc.set_bot_commands import set_default_commands
from tgbot.misc.start_notification import start_notification
from tgbot.misc.closing_notificatoin import closing_notification

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):

    register_newChat(dp)
    register_new_user(dp)
    register_admin_on_private(dp)
    register_admin(dp)
    register_user(dp)
    register_ban_words(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await set_default_commands(dp)
        await start_notification(dp)
        await dp.start_polling()
    finally:
        await closing_notification(dp)
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
