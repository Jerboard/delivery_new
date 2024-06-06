from aiogram.types import ErrorEvent

import db
from init import dp, bot, log_error


@dp.errors()
async def errors_handler(ex: ErrorEvent):
    msg = log_error(ex)

    user_id = ex.update.message.chat.id if ex.update.message else 0
    await db.save_error(user_id, msg)

    if user_id:
        await bot.send_message(
            chat_id=user_id,
            text='‼️ Что-то сломалось! Сообщите разработчикам, чтоб мы могли это исправить\n\n'
                 'В сообщении расскажите о ваших последних действиях')

