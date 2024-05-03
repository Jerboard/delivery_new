from datetime import datetime

import db
from init import bot, TZ
from config import config
import keyboards as kb
from utils import text_utils as txt
from utils import redis_utils as rds
from enums import UserActions, UserRole


# старт курьера
async def delivery_start(user_id: int, dlv_name: str, msg_id: int = None):
    orders = await db.get_orders(dlv_name=dlv_name, get_active=True)

    orders_text = ''
    counter = 0
    for order in orders:
        counter += 1
        orders_text += txt.get_short_order_row(order, for_=UserRole.DLV.value)

    text = f'{dlv_name}\n\n' \
           f'Заказы:\n' \
           f'{orders_text}'

    if counter == 0:
        text = 'У вас нет активных заказов'

    if msg_id:
        await bot.edit_message_text(text, chat_id=user_id, message_id=msg_id)
    else:
        await bot.send_message (user_id, text)


async def get_profile_dlv(user_id: int, user_info: db.UserRow = None, msg_id: int = None):
    if not user_info:
        user_info = await db.get_user_info (user_id)

    statistic = await db.get_statistic_dlv (user_id=user_id)
    statistic_text = txt.get_statistic_text (statistic)
    text = f'{user_info.name}\n\n{statistic_text}'

    if msg_id:
        await bot.edit_message_text (text, reply_markup=kb.main_dvl_kb (), chat_id=user_id, message_id=msg_id)
    else:
        await bot.send_message (user_id, text, reply_markup=kb.main_dvl_kb ())


async def save_expenses(
        user_id: int,
        data: dict
):
    user_info = await db.get_user_info (user_id)

    today_str = datetime.now (TZ).strftime (config.day_form)
    exp_today = await db.get_report_dlv(user_info.name, today_str)

    comment = f'{data["exp_sum"]} - {data["comment"]}'

    if exp_today:
        comment_list: list = exp_today.l
        comment_list.append(comment)
        await db.update_expenses_dlv(
            entry_id=exp_today.id,
            l=comment,
            b=exp_today.b + (data.get('b', 0)),
            c=exp_today.c + (data.get('c', 0)),
            d=exp_today.d + (data.get('d', 0)),
            e=exp_today.e + (data.get('e', 0)),
            f=exp_today.f + (data.get('f', 0)),
            g=exp_today.g + (data.get('g', 0)),
            h=exp_today.h + (data.get('h', 0)),
            i=exp_today.i + (data.get('i', 0)),
            k=exp_today.k + (data.get('k', 0)),
        )

    else:
        last_row = await db.get_last_updated_report(last_row=True)
        print(last_row)
        row_num = last_row.row_num + 1 if last_row.m == today_str else last_row.row_num + 2
        await db.add_report_row (
            l=[comment],
            m=today_str,
            n=user_info.name,
            b=data.get('b', 0),
            c=data.get('c', 0),
            d=data.get('d', 0),
            e=data.get('e', 0),
            f=data.get('f', 0),
            g=data.get('g', 0),
            h=data.get('h', 0),
            i=data.get('i', 0),
            k=data.get('k', 0),
            row_num=row_num
        )

    today = datetime.now (TZ).strftime (config.time_form)
    text = (f'Курьер: {user_info.name}\n'
            f'Время: {today}\n'
            f'Сумма: {data["exp_sum"]} ₽\n'
            f'Комментарий: {data["comment"]}')

    if data.get('photo_id'):
        await bot.send_photo (config.group_expenses, photo=data['photo_id'], caption=text)
    else:
        await bot.send_message (config.group_expenses, text)

    await bot.send_message (user_id, '✅Ваша трата учтена')
    await db.save_user_action(user_id, user_info.name, UserActions.ADD_EXPENSES.value, text)
