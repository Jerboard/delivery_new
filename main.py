import asyncio
import logging
import sys

from handlers import dp
from config import DEBUG
from init import set_main_menu, bot, log_error
from db.base import init_models, create_trigger
from utils.schedulers_util import start_scheduler, check_take_orders
from utils.local_data_utils import create_local_data_files

from google_api.base_google import save_new_order_table
from utils.base_utils import get_dlv_name_dict, get_work_orders_list


async def main() -> None:
    create_local_data_files()
    # await create_trigger()
    await init_models()
    await set_main_menu()
    if not DEBUG:
        # await create_trigger()
        await start_scheduler()
    # await start_scheduler ()
    await bot.delete_webhook (drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    if DEBUG:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    else:
        log_error('start_bot', with_traceback=False)
    asyncio.run(main())
