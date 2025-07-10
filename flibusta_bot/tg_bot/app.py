from aiogram import types as tg_types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from loguru import logger

from .. import config
from .bot import bot, dp
from .handlers import register_handlers


class App:
    def __init__(self):
        self.bot = bot
        self.dp = dp

        self.dp.startup.register(self.on_startup)
        self.dp.shutdown.register(self.on_shutdown)

    async def on_startup(self):
        await self.bot.set_my_commands(
            [
                tg_types.BotCommand(command="start", description="Start the bot"),
            ],
        )
        register_handlers(self.dp)
        await self.bot.delete_webhook(drop_pending_updates=True)

        if config.TG_BOT_WEBHOOK_BASE_URL:
            await self.bot.set_webhook(
                f"{config.TG_BOT_WEBHOOK_BASE_URL}{config.TG_BOT_WEBHOOK_PATH}",
                secret_token=config.TG_BOT_WEBHOOK_SECRET,
            )
        else:
            await self.bot.delete_webhook(drop_pending_updates=True)

    async def on_shutdown(self):
        logger.info("Shutting down the bot")

    def run(self):
        logger.info("Starting Bot...")

        if not config.TG_BOT_WEBHOOK_BASE_URL:
            self.dp.run_polling(self.bot)
        else:
            web_app = web.Application()
            webhook_request_handler = SimpleRequestHandler(
                dispatcher=self.dp,
                bot=self.bot,
                secret_token=config.TG_BOT_WEBHOOK_SECRET,
            )
            webhook_request_handler.register(web_app, path=config.TG_BOT_WEBHOOK_PATH)
            setup_application(web_app, self.dp, bot=self.bot)
            web.run_app(
                web_app, host=config.WEB_SERVER_HOST, port=config.WEB_SERVER_PORT
            )
