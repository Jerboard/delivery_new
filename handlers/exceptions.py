from aiogram.types import ErrorEvent

import db
from init import dp, bot, log_error


@dp.errors()
async def errors_handler(ex: ErrorEvent):
    log_error(ex)

    msg = ex.split ('\n\n') [-1]
    user_id = ex.update.message.chat.id if ex.update.message else 0
    await db.save_error(user_id, msg)
