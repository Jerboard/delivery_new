from datetime import datetime, timedelta

import db
import keyboards as kb
from init import scheduler, TZ, bot, log_error
from config import Config
from google_api import update_google_row
from utils import local_data_utils as dt
from enums import DataKey


# Запускает плпнировцики
async def start_scheduler():
    scheduler.add_job(update_google_row, 'interval', seconds=3)
    scheduler.add_job(check_take_orders, 'interval', minutes=5)
    scheduler.add_job(check_take_orders, 'cron', hour=0)
    scheduler.start()


async def resent_take_order(order_id: int, text: str, sent_list: list[dict]):
    for dlv in sent_list:
        try:
            await bot.send_message (
                chat_id=dlv['user_id'],
                text=text,
                reply_markup=kb.get_free_order_kb (order_id=order_id, is_take=True))
        except Exception as ex:
            log_error (f'Заказ не отправлен курьеру повторно {dlv["user_id"]}', with_traceback=False)
            log_error (ex)


async def check_take_orders():
    orders = dt.get_opr_msg_data()

    one_hour_ago = datetime.now(TZ) - timedelta(hours=1)
    for key, order in orders.items():
        created = TZ.localize(datetime.strptime(order['updated_at'], Config.datetime_form))
        if created < one_hour_ago:
            await resent_take_order(
                order_id=order['order_id'],
                text=order['text'],
                sent_list=order['sent_list'],
            )
            order['updated_at'] = datetime.now(TZ).replace(microsecond=0).strftime(Config.datetime_form)
            dt.save_opr_msg_data(key=key, new_data=order)


# обновляет дату у заказов на руках
async def update_order_date():
    now_str = datetime.now (TZ).strftime(Config.day_form)
    await db.update_multi_orders(date_str=now_str)