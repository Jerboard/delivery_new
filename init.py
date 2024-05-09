from aiogram import Dispatcher
from aiogram.types.bot_command import BotCommand
from aiogram import Bot
from aiogram.enums import ParseMode

from pytz import timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import create_async_engine
from datetime import datetime
from redis import Redis

import logging
import traceback
import os
import asyncio

from config import Config


try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except:
    pass


loop = asyncio.get_event_loop()
dp = Dispatcher()
bot = Bot(Config.token, parse_mode=ParseMode.HTML)
TZ = timezone(Config.tz)

scheduler = AsyncIOScheduler(timezone=TZ)

ENGINE = create_async_engine(url=Config.db_url)

# redis_client = Redis(host=Config.host, port=Config.redis_port, db=Config.redis_db)


async def set_main_menu():
    main_menu_commands = [
        BotCommand(command='/start', description='Главный экран'),
        BotCommand(command='/main', description='ЛК курьера'),
    ]

    await bot.set_my_commands(main_menu_commands)


# запись ошибок
def log_error(message, with_traceback: bool = True):
    now = datetime.now(TZ)
    log_folder = now.strftime ('%m-%Y')
    log_path = os.path.join('logs', log_folder)

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    log_file_path = os.path.join(log_path, f'{now.day}.log')
    logging.basicConfig (level=logging.WARNING, filename=log_file_path, encoding='utf-8')
    if with_traceback:
        ex_traceback = traceback.format_exc()
        logging.warning(f'{now}\n{ex_traceback}\n{message}\n---------------------------------')
    else:
        logging.warning(f'{now}\n{message}\n---------------------------------')
