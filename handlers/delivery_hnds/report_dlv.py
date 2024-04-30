from aiogram.types import Message, CallbackQuery

import db
import keyboards as kb
from init import dp, bot, TZ, log_error
from config import config
from enums import DeliveryCB, OrderStatus, UserActions


# отчёт по дням
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.DLV_ORDER_1.value))
async def dlv_order_1(cb: CallbackQuery):
    user_info = await db.get_user_info(user_id=cb.from_user.id)
    dlv_reports = await db.get_reports_all_dlv(dlv_name=user_info.name)

    await cb.message.edit_reply_markup(reply_markup=kb.report_view_days_kb(dlv_reports))


# отчёт за день
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.DLV_ORDER_2.value))
async def dlv_order_2(cb: CallbackQuery):
    _, date_str = cb.data.split(':')

    user_info = await db.get_user_info (user_id=cb.from_user.id)
    dlv_orders = await db.get_orders(dlv_name=user_info.name, on_date=date_str)
    dlv_report = await db.get_report_dlv(dlv_name=user_info.name, exp_date=date_str)

    suc_text, refuse_text, active_text, not_come = '', '', '', ''
    cost_prod, cost_dlv, discount = 0, 0, 0

    for order in dlv_orders:
        prepay = order.u + order.v

        if order.q == 0 and prepay != 0:
            cost = 0
        else:
            cost = order.q + order.r + order.clmn_t - order.y

        comment = f'({order.ab})' if order.ab is not None else ''
        row_text = f'{order.g} {order.n}  {cost} + {order.s} {order.w} {comment}\n'

        if order.g == OrderStatus.SUC.value:
            cost_prod += cost
            discount += order.y
            suc_text = f'{suc_text}{row_text}{comment}'

        elif order.g == OrderStatus.REF.value:
            refuse_text = f'{refuse_text}{row_text}'

        elif order.g == OrderStatus.ACTIVE.value:
            active_text = f'{active_text}{row_text}'

        elif order.g == OrderStatus.NOT_COME.value:
            not_come = f'{not_come}{row_text}'

    total_expenses = (dlv_report.b + dlv_report.c + dlv_report.d + dlv_report.e + dlv_report.f + dlv_report.g +
                      dlv_report.h + dlv_report.i + dlv_report.j)
    cost_prod = cost_prod - discount
    total = cost_prod - total_expenses

    spt = '\n---------------------------\n'
    text = (f'{user_info.name}\n\n'
            f'{date_str}\n\n'
            f'{suc_text}{spt}{refuse_text}{spt}{active_text}{spt}{not_come}{spt}'
            f'Касса: {cost_prod}\n\n'
            f'{dlv_report.l}\n\n'
            f'Итог: {total}')

    await cb.message.answer(text, reply_markup=kb.get_send_day_report_kb())

    await db.save_user_action(user_id=cb.from_user.id, dlv_name=user_info.name, action=UserActions.VIEW_REPORT.value)


# подтверждение отчёта
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.DLV_ORDER_3.value))
async def expenses_dvl_view(cb: CallbackQuery):
    cb_data = cb.data.split(':')

    text = f'‼️Перед отправкой отчёта проверьте траты'

    await cb.message.edit_reply_markup(reply_markup=get_day_report_kb_2(cb_data[1], cb_data[2]))
    await cb.answer(text, show_alert=True)


# отчёт за день. Отправляет в группу
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.DLV_ORDER_4.value))
async def expenses_dvl_view(cb: CallbackQuery):
    user_info = await db.get_user_info(user_id=cb.from_user.id)

    await bot.send_message(config.group_report, cb.message.text)
    await cb.message.edit_text(f'{cb.message.text}\n\n✅ Отчёт отправлен')
    await db.save_user_action (user_id=cb.from_user.id, dlv_name=user_info.name, action=UserActions.SEND_REPORT.value)
