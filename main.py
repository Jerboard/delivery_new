import asyncio
import logging
import sys

from handlers import dp
from config import DEBUG
from init import set_main_menu, bot, log_error
from db.base import init_models
from utils.schedulers_util import start_scheduler, check_take_orders

from google_api.base_google import save_new_order_table


async def main() -> None:
    # await check_take_orders()
    await init_models()
    await set_main_menu()
    await start_scheduler()
    await bot.delete_webhook (drop_pending_updates=True)
    await dp.start_polling(bot)
    print ('>>>>>stop 1')
    # await bot.session.close()
    print('>>>>>stop 2')


if __name__ == "__main__":
    if DEBUG:
        logging.basicConfig(level=logging.WARNING, stream=sys.stdout)
    else:
        log_error('start_bot', with_traceback=False)
    asyncio.run(main())
