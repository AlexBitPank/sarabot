import asyncio
import logging
import sys
import app.data_base as db
from app.handlers import router
from app import data_base
from create_bot import dp, bot

async def main() -> None:
    dp.include_router(router)
    await data_base.create_pool()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())