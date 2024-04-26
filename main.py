import asyncio
import logging
import sys

from handlers import dp
from config import DEBUG
from init import set_main_menu, bot, log_error
from db.base import init_models

from google_api.base_google import save_new_report_table


async def main() -> None:
    # await save_new_report_table()
    await init_models()
    await set_main_menu()
    await bot.delete_webhook (drop_pending_updates=True)
    await dp.start_polling(bot)
    await bot.session.close()


if __name__ == "__main__":
    if DEBUG:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    else:
        log_error('start_bot', with_traceback=False)
    asyncio.run(main())
