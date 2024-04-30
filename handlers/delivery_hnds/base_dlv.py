from datetime import datetime

import db
from init import bot, TZ
from config import config
import keyboards as kb
from utils.base_utils import hand_digit
from enums import UserActions


# старт курьера
async def delivery_start(user_id: int, dlv_name: str, msg_id: int = None):
    orders = await db.get_orders(dlv_name=dlv_name, get_active=True)

    orders_text = ''
    counter = 0
    for order in orders:
        counter += 1
        prepay = order.u + order.v

        if order.q == 0 and prepay != 0:
            cost = 0
        else:
            cost = order.q + order.r + order.clmn_t - order.y

        orders_text = (f'{orders_text}'
                       f'<code>{order.n}</code>  <code>{order.o}</code> {cost} + {order.s} {order.aa}'
                       f'\n---------------------------\n')

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

    cnt_stat = await db.count_status_orders (dlv=user_info.name)

    text = f'{user_info.name}\n\n' \
           f'Всего заказов: {cnt_stat [0]}\n' \
           f'Доставлено: {int (cnt_stat [3]) + int (cnt_stat [4])}\n' \
           f'На руках: {cnt_stat [2]}\n' \
           f'Отказ: {cnt_stat [5] + cnt_stat [7]}\n'

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
    if exp_today:
        # update_comment = f'{exp_today.l}\n{data["comment"]}'
        update_comment = exp_today.l.append(data["comment"])
        await db.update_expenses_dlv(
            entry_id=exp_today.id,
            l=update_comment,
            b=exp_today.b + (data.get('b') if data.get('b') else 0),
            c=exp_today.c + (data.get('c') if data.get('c') else 0),
            d=exp_today.d + (data.get('d') if data.get('d') else 0),
            e=exp_today.e + (data.get('e') if data.get('e') else 0),
            f=exp_today.f + (data.get('f') if data.get('f') else 0),
            g=exp_today.g + (data.get('g') if data.get('g') else 0),
            h=exp_today.h + (data.get('h') if data.get('h') else 0),
            i=exp_today.i + (data.get('i') if data.get('i') else 0),
            k=exp_today.k + (data.get('k') if data.get('k') else 0)
        )

    else:
        await db.add_report_row (
            l=data["comment"],
            m=today_str,
            n=user_info.name,
            b=data.get('b'),
            c=data.get('c'),
            d=data.get('d'),
            e=data.get('e'),
            f=data.get('f'),
            g=data.get('g'),
            h=data.get('h'),
            i=data.get('i'),
            k=data.get('k')
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
