

import db
import keyboards as kb
from init import bot
from utils import text_utils as txt


async def owner_start(user_id: int):
    statistic = await db.get_orders_statistic ()
    statistic_text = txt.get_statistic_text (statistic)
    text = f'Заказы\n\n{statistic_text}'

    await bot.send_message (user_id, text, reply_markup=kb.main_owner_kb ())
