

import db
import keyboards as kb
from init import bot


async def owner_start(user_id: int):
    cnt_stat = await db.count_status_orders ()

    text = f'Заказы:\n\n' \
           f'Всего: {cnt_stat [0]}\n' \
           f'Доставлено: {int (cnt_stat [3]) + int (cnt_stat [4])}\n' \
           f'На руках: {cnt_stat [2]}\n' \
           f'Отказ: {cnt_stat [5] + cnt_stat [7]}\n' \
           f'Отправлено: {cnt_stat [6]}\n' \
           f'Без курьера: {cnt_stat [1]}'

    await bot.send_message (user_id, text, reply_markup=kb.main_owner_kb ())
