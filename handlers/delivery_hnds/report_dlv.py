from aiogram.types import Message, CallbackQuery

from datetime import datetime

import db
import keyboards as kb
from init import dp, bot, TZ, log_error
from config import Config
from utils.base_utils import get_order_cost
from utils.text_utils import get_short_order_row
from data import base_data as dt
from enums import DeliveryCB, OrderStatus, UserActions, ShortText, Letter


# отчёт по дням
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.REPORT_1.value))
async def report_dvl_1(cb: CallbackQuery):
    user_info = await db.get_user_info(user_id=cb.from_user.id)
    date_str = datetime.now (TZ).date ().strftime (Config.day_form)
    dlv_reports = await db.get_reports_all_dlv(dlv_name=user_info.name, exception_date=date_str)

    await cb.message.edit_reply_markup(reply_markup=kb.report_view_days_kb(dlv_reports))


# 6600572025 - мияги, 5766385456 - Ян, 5051573626 - Мел
# отчёт за день
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.REPORT_2.value))
async def report_dvl_2(cb: CallbackQuery):
    _, date_str = cb.data.split(':')

    user_info = await db.get_user_info (user_id=cb.from_user.id)
    # user_info = await db.get_user_info (user_id=6600572025)
    if date_str == 'today':
        date_str = datetime.now(TZ).date().strftime(Config.day_form)
        dlv_orders = await db.get_work_orders(cb.from_user.id)
        # dlv_orders = await db.get_work_orders(6600572025)

    else:
        dlv_orders = await db.get_orders(dlv_name=user_info.name, on_date=date_str)

    dlv_report = await db.get_report_dlv(dlv_name=user_info.name, exp_date=date_str)

    suc_text, refuse_text, active_text, not_come = '', '', '', ''
    cost_prod, cost_dlv = 0, 0
    salary = {Letter.D.value: 0, Letter.V.value: 0, Letter.A.value: 0, }

    for order in dlv_orders:
        row_text = get_short_order_row(order=order, for_=ShortText.REPORT.value)

        if order.g == OrderStatus.SUC.value:
            cost = get_order_cost(order, with_t=True)
            cost_prod += cost
            suc_text += row_text
            summary = salary.get(order.d, 0)
            # print(summary)
            # if summary:
            salary[order.d] = summary + 1

        elif order.g == OrderStatus.REF.value:
            refuse_text += row_text

        elif order.g == OrderStatus.ACTIVE.value:
            active_text += row_text

        elif order.g == OrderStatus.NOT_COME.value:
            not_come = f'{not_come}{row_text}'
            not_come += row_text

    # print(dlv_report)
    if dlv_report:
        # print(dlv_report.b, dlv_report.c, dlv_report.d, dlv_report.e, dlv_report.f, dlv_report.g, dlv_report.h, dlv_report.i, dlv_report.j, dlv_report.k)
        total_expenses = (dlv_report.b + dlv_report.c + dlv_report.d + dlv_report.e + dlv_report.f + dlv_report.g +
                          dlv_report.h + dlv_report.i + dlv_report.j + dlv_report.k)
    else:
        total_expenses = 0

    salary_str = ''
    for k, v in salary.items():
        if v:
            salary_str += f'{dt.letters.get(k)} - {v}\n'

    total = cost_prod - total_expenses
    expenses = '\n'.join(dlv_report.l) if dlv_report else ''

    spt = '\n---------------------------\n'
    text = (f'{user_info.name}\n\n'
            f'{date_str}\n'
            f'{salary_str}\n'
            f'{suc_text}{spt}{refuse_text}{spt}{active_text}{spt}{not_come}{spt}'
            f'Касса: {cost_prod}\n\n'
            f'{expenses}\n\n'
            f'Итог: {total}')

    await cb.message.answer(text, reply_markup=kb.get_send_day_report_kb())

    await db.save_user_action(user_id=cb.from_user.id, dlv_name=user_info.name, action=UserActions.VIEW_REPORT.value)


# подтверждение отчёта
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.REPORT_3.value))
async def report_dvl_3(cb: CallbackQuery):
    text = f'‼️Перед отправкой отчёта проверьте траты'

    await cb.message.edit_reply_markup(reply_markup=kb.get_day_report_kb())
    await cb.answer(text, show_alert=True)


# Отчёт за день. Отправляет в группу
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.REPORT_4.value))
async def report_dvl_4(cb: CallbackQuery):
    user_info = await db.get_user_info(user_id=cb.from_user.id)

    await bot.send_message(Config.work_chats['group_report'], cb.message.text)
    await cb.message.edit_text(f'{cb.message.text}\n\n✅ Отчёт отправлен')
    active_orders = await db.get_orders (dlv_name=user_info.name, get_active=True)

    except_list = [row.id for row in active_orders]
    await db.delete_work_order(user_id=cb.from_user.id, except_list=except_list)

    await db.save_user_action (user_id=cb.from_user.id, dlv_name=user_info.name, action=UserActions.SEND_REPORT.value)
