import asyncio
import re

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from datetime import datetime

import db
import keyboards as kb
from init import dp, bot, log_error, TZ
from config import Config
from utils import local_data_utils as dt
from data.base_data import company
from enums import OperatorCB, OperatorStatus, TypeOrderUpdate, OrderStatus, DataKey


# кнопка взять заказ
@dp.callback_query(lambda cb: cb.data.startswith(OperatorCB.TAKE_ORDER_1.value))
async def take_order_1(cb: CallbackQuery, state: FSMContext):
    _, comp_id = cb.data.split (':')

    text = f'Чтобы отправить заявку на забор курьерам - подставьте данные в форму \n\n' \
           f'<code>Оператор:\n' \
           f'Партнер:\n' \
           f'ФИО:\n' \
           f'Номер:\n' \
           f'Забрать:\n' \
           f'Цена:\n' \
           f'Доставка:\n' \
           f'Метро:\n' \
           f'Адрес:\n' \
           f'Примечание: </code>'

    await state.set_state (OperatorStatus.TAKE_ORDER)
    sent = await cb.message.answer (text, reply_markup=kb.get_take_order_kb())
    await state.update_data (data={'msg_id': sent.message_id, 'comp_id': comp_id})


@dp.message (StateFilter(OperatorStatus.TAKE_ORDER))
async def take_order(msg: Message, state: FSMContext):
    await msg.delete ()
    data = await state.get_data ()
    await bot.edit_message_text (
        text=msg.text,
        chat_id=msg.chat.id,
        message_id=data ['msg_id'],
        reply_markup=kb.get_take_order_kb(True)
    )


# кнопка взять заказ
@dp.callback_query(lambda cb: cb.data.startswith(OperatorCB.TAKE_ORDER_2.value))
async def take_order_2(cb: CallbackQuery, state: FSMContext):
    sent_wait = await cb.message.answer ('⏳')
    data = await state.get_data ()
    await state.clear ()

    last_row = await db.get_max_row_num ()
    data_text = cb.message.text.split ('\n')
    order_id = await db.add_row(
        row_num=last_row + 1,
        g=OrderStatus.NEW.value,
        k=data_text[0].replace('Оператор:', '').strip(),
        l=data_text[1].replace('Партнер:', '').strip(),
        m=data_text[2].replace('ФИО:', '').strip(),
        n=data_text[3].replace('Номер:', '').strip(),
        p=data_text[4].replace('Забрать:', '').strip(),
        q=int(re.sub (r'\D+', '', data_text[5])),
        t=int(re.sub (r'\D+', '', data_text[6])),
        w=data_text[7].replace('Метро:', '').strip(),
        x=data_text[8].replace('Адрес:', '').strip(),
        ab=data_text[9].replace('Примечание:', '').strip(),
        ac=company.get(data ['comp_id'], 'н/д'),
        type_update=TypeOrderUpdate.ADD_OPR.value
    )

    dlvs = await db.get_users(company=data ['comp_id'])

    sent_list = []
    for dlv in dlvs:
        try:
            sent = await bot.send_message (
                chat_id=dlv.user_id,
                text=cb.message.text,
                reply_markup=kb.get_free_order_kb(order_id=order_id, is_take=True)
            )
            sent_list.append ({'user_id': sent.chat.id, 'message_id': sent.message_id})
            await asyncio.sleep (0.05)
        except Exception as ex:
            log_error(f'Заказ не отправлен курьеру {dlv.name}', with_traceback=False)
            log_error(ex)

    now_str = datetime.now(TZ).replace(microsecond=0).strftime(Config.datetime_form)
    key = f'{DataKey.ADD_OPR_ORDER.value}-{order_id}'
    order_data = {
        'opr': cb.from_user.id,
        'order_id': order_id,
        'created_at': now_str,
        'updated_at': now_str,
        # 'company_id': data ['comp_id'],
        'sent_list': sent_list,
        'text': cb.message.text
    }
    dt.save_opr_msg_data(key, new_data=order_data)
    text = f'✅Заявка добавлена.\n\n{cb.message.text}'
    await sent_wait.edit_text(text)

    await bot.send_message (Config.work_chats[data['comp_id']], cb.message.text)
