import asyncio
from aiogram import Bot, Dispatcher
from config_reader import config
from handlers.user_commands import router
bot = Bot(config.bot_token.get_secret_value())


async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
