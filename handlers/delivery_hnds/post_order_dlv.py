from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from datetime import datetime
from asyncio import sleep

import db
import keyboards as kb
from init import dp, bot, log_error
from handlers.operator_hnds.base_opr import send_opr_report_msg
from config import Config
from utils import local_data_utils as dt
from utils import text_utils as txt
from data.base_data import work_chats, order_actions
from enums import (DeliveryCB, OrderStatus, DataKey, UserActions, DeliveryStatus, OrderAction, TypeOrderUpdate,
                   TypeOrderButton)


# запрашивает трек номер
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.POST_1.value))
async def post_1(cb: CallbackQuery, state: FSMContext):
    _, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    await state.set_state(DeliveryStatus.POST_ID)
    await state.update_data(data={
        'order_id': order_id,
        'msg_id': cb.message.message_id
    })
    await cb.message.answer('Отправьте трек заказа', reply_markup=kb.get_close_kb())


# Изменяет заказ на отправлен
@dp.message (StateFilter (DeliveryStatus.POST_ID))
async def post_id(msg: Message, state: FSMContext):
    data = await state.get_data ()
    await state.clear ()

    # добавить смену курьерской
    await db.update_row_google(
        order_id=data['order_id'],
        status=OrderStatus.SEND.value,
        type_update=TypeOrderUpdate.STATE.value,
        note=msg.text
    )
    order_info = await db.get_order(data['order_id'])

    await bot.edit_message_reply_markup (chat_id=msg.chat.id, message_id=data['msg_id'], reply_markup=None)
    await msg.answer('✅ Заказ отправлен')

    # отправить трек оператору
    await send_opr_report_msg(order_info)

    # журнал действий
    await db.save_user_action(
        user_id=msg.from_user.id,
        dlv_name=order_info.f,
        action=UserActions.SEND_POST_ORDER.value,
        comment=f'{data["order_id"]}'
    )


# Заказ доставлен
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.POST_2.value))
async def post_2(cb: CallbackQuery, state: FSMContext):
    _, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    user_info = await db.get_user_info (cb.from_user.id)
    await db.update_row_google(
        order_id=order_id,
        status=OrderStatus.REF.value,
        type_update=TypeOrderUpdate.STATE.value,
    )
    await cb.message.edit_text(
        text=f'{cb.message.text}\n\n❌ Отказ',
        entities=cb.message.entities
    )
    # журнал действий
    await db.save_user_action(
        user_id=cb.from_user.id,
        dlv_name=user_info.name,
        action=UserActions.SEND_POST_ORDER.value,
        comment=str(order_id)
    )

