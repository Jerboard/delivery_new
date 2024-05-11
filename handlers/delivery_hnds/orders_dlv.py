from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from datetime import datetime
from asyncio import sleep

import db
import keyboards as kb
from init import dp, bot, TZ, log_error
from config import Config
from utils import local_data_utils as dt
from utils.text_utils import get_order_text
from data.base_data import order_status_data, order_actions
from enums import DeliveryCB, OrderStatus, DataKey, UserActions, DeliveryStatus, OrderAction, TypeOrderUpdate


# кнопка взять заказ
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.ORDER_1.value))
async def dlv_order_1(cb: CallbackQuery):
    # _, row_num, order_id = map(int, cb.data.split(':')[1:])
    _, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    user_info = await db.get_user_info(cb.from_user.id)
    take_date = datetime.now(TZ).date().strftime(Config.day_form)

    await db.add_work_order(user_id=cb.from_user.id, order_id=order_id)
    await db.update_row_google(
        order_id=order_id,
        dlv_name=user_info.name,
        status=OrderStatus.ACTIVE.value,
        take_date=take_date,
        type_update=TypeOrderUpdate.STATE.value
    )
    await cb.message.edit_text(
        text=f'{cb.message.text}\n\n✅Принят',
        entities=cb.message.entities,
        parse_mode=None
    )

    # журнал действий
    await db.save_user_action(
        user_id=cb.from_user.id,
        dlv_name=user_info.name,
        action=UserActions.TAKE_ORDER.value,
        # comment=f'Строка {row_num}'
    )


# взять заказ на забор
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.TAKE_ORDER_2.value))
async def dlv_order_2(cb: CallbackQuery):
    # _, row_num, order_id = map (int, cb.data.split (':') [1:])
    _, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    order = await db.get_order(order_id)
    if not order:
        await cb.message.answer('❗️ОШИБКА. Что-то пошло не так - обратитесь к оператору')

    elif order.g != OrderStatus.NEW.value:
        await cb.message.answer ('❗️ОШИБКА. Заказ уже взял другой курьер')

    else:
        user_info = await db.get_user_info (cb.from_user.id)

        take_date = datetime.now (TZ).date ().strftime (Config.day_form)
        await db.add_work_order(user_id=cb.from_user.id, order_id=order_id)
        await db.update_row_google (
            order_id=order_id,
            dlv_name=user_info.name,
            status=OrderStatus.ACTIVE_TAKE.value,
            take_date=take_date
        )

        key = f'{DataKey.ADD_OPR_ORDER.value}-{order_id}'
        data_order = dt.get_opr_msg_data(key)
        dt.del_opr_msg_data(key)
        for msg in data_order['sent_list']:
            try:
                await bot.delete_message(chat_id=msg['user_id'], message_id=msg['message_id'])
            except Exception as ex:
                print(ex)
                # log_error(ex)

        opr_info = await db.get_user_info(name=order.k)

        await cb.message.edit_text(
            text=f'{cb.message.text}\n\n✅ Принят',
            entities=cb.message.entities,
            parse_mode=None
        )
        text = f'✅Заказ принят. {user_info.name}\n\n{cb.message.text}'
        await bot.send_message(opr_info.user_id, text)
        # журнал действий
        await db.save_user_action(
            user_id=cb.from_user.id,
            dlv_name=user_info.name,
            action=UserActions.TAKE_ORDER_TAKE.value,
            comment=str(order_id))


# Подтвердить доставку либо отмену заказа
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.ORDER_2.value))
async def dlv_order_2(cb: CallbackQuery):
    _, action, order_id_str = cb.data.split(':')
    order_id = int(order_id_str)

    if action == OrderAction.SUC.value:
        await cb.message.edit_reply_markup(reply_markup=kb.get_close_order_option_kb(order_id=order_id))

    elif action == OrderAction.NOT_COME.value:
        await db.update_row_google(
            order_id=order_id,
            note=order_status_data.get(OrderStatus.NOT_COME.value)
        )
        await cb.message.edit_text(
            text=f'{cb.message.text}\n\n✖️ Клиент не явился',
            entities=cb.message.entities,
            parse_mode=None
        )

    else:
        await cb.answer('Нажмите кнопку "Подтвердить отказ", после этого заказ будет закрыт', show_alert=True)
        await cb.message.edit_reply_markup(
            reply_markup=kb.get_close_order_kb(new_status_order=OrderStatus.REF.value, order_id=order_id))


# закрытие заказа
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.ORDER_4.value))
async def dlv_order_4(cb: CallbackQuery):
    _, new_order_status, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    order_info = await db.get_order (order_id)

    if new_order_status in [OrderStatus.SUC.value, OrderStatus.SUC_TAKE.value]:
        # тут буковку надо ещё добавить
        await db.update_row_google (
            order_id=order_id,
            status=new_order_status,
            type_update=TypeOrderUpdate.STATE.value
        )
        await cb.message.edit_text(
            text=f'{cb.message.text}\n\n✅Выполнен',
            entities=cb.message.entities,
            parse_mode=None
        )

        action = UserActions.SUCCESS_ORDER.value
        if new_order_status == OrderStatus.SUC_TAKE.value:
            opr_info = await db.get_user_info (name=order_info.k)
            text = f'✅Заказ получен курьером\n\n{cb.message.text}'
            await bot.send_message(opr_info.user_id, text)
            action = UserActions.SUCCESS_TAKE_ORDER.value

        # журнал действий
        await db.save_user_action (
            user_id=cb.from_user.id,
            dlv_name=order_info.f,
            action=action,
            comment=order_id_str)

    else:
        await db.update_row_google (
            order_id=order_id,
            status=new_order_status,
            type_update=TypeOrderUpdate.STATE.value
        )
        await cb.message.edit_text(
            text=f'{cb.message.text} ✖️Отказ',
            entities=cb.message.entities,
            parse_mode=None
        )

        # журнал действий
        await db.save_user_action(
            user_id=cb.from_user.id,
            dlv_name=order_info.f,
            action=UserActions.REFUSE_ORDER.value,
            comment=order_id_str)


# закрытие заказа с изминениями. Запрос суммы изминений
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.ORDER_6.value))
async def dlv_order_6(cb: CallbackQuery, state: FSMContext):
    _, action, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    await state.set_state(DeliveryStatus.EDIT_ORDER_CLOSE_1)
    await state.update_data(data={'order_id': order_id, 'action': action})

    if action == OrderAction.COST.value:
        text = '📝 Введите сумму скидки'
    else:
        text = '📝 Введите фактическую стоимость доставки'

    await cb.message.answer(text, reply_markup=kb.get_close_kb())


# закрытие заказа с изминениями. Запрос причины изминений
@dp.message(StateFilter(DeliveryStatus.EDIT_ORDER_CLOSE_1))
async def edit_order_close_1(msg: Message, state: FSMContext):

    if msg.text.isdigit():
        data = await state.get_data()

        if data['action'] == OrderAction.COST.value:
            await state.update_data(data={'discount': int(msg.text)})
        else:
            await state.update_data(data={'cost': msg.text, 'discount': int(msg.text)})

        await state.set_state(DeliveryStatus.EDIT_ORDER_CLOSE_2)
        sent = await msg.answer('Причина изменения стоимости')
        # await state.update_data(data={'msg2': sent.message_id, 'msg3': msg.message_id})

    else:
        sent = await msg.answer('‼️Отправьте целое число')
        await sleep(3)
        await sent.delete()


# закрытие заказа с изменениями. закрытие
@dp.message(StateFilter(DeliveryStatus.EDIT_ORDER_CLOSE_2))
async def edit_order_close_2(msg: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    note = f' {order_actions.get(data["action"])} ({data ["discount"]}) {msg.text}'
    if data['action'] == OrderAction.COST.value:
        await db.update_row_google(
            order_id=data['order_id'],
            type_update=data['action'],
            discount=data['discount'],
            note=note
        )
        # журнал действий
        user_action = UserActions.ADD_DISCOUNT.value
    else:
        await db.update_row_google (
            order_id=data ['order_id'],
            type_update=data['action'],
            cost_delivery=data ['discount'],
            note=note
        )

        # журнал действий
        user_action = UserActions.ADD_DISCOUNT_DLV.value

    order_info = await db.get_order(data['order_id'])
    text = get_order_text(order_info)
    await msg.answer(text, reply_markup=kb.get_close_order_option_kb(data['order_id']))

    # журнал действий
    await db.save_user_action(
        user_id=msg.from_user.id,
        dlv_name=order_info.f,
        action=user_action,
        comment=f'ID {data["order_id"]}')


# кнопка передать заказ
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.ORDER_3.value))
async def dlv_order_3(cb: CallbackQuery):
    _, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    user_info = await db.get_user_info(cb.from_user.id)
    delivers = await db.get_users(exc_user_id=cb.from_user.id, company=user_info.company)

    await cb.message.edit_reply_markup(reply_markup=kb.get_transfer_order_kb(delivers, order_id))
    
    
# передаёт заказ
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.TRANS_ORDER.value))
async def trans_order(cb: CallbackQuery, state: FSMContext):
    user_id, order_id = map(int, cb.data.split(':')[1:])

    user = await db.get_user_info(cb.from_user.id)
    recip = await db.get_user_info(user_id)

    await db.update_row_google (
        order_id=order_id,
        dlv_name=recip.name,
        type_update=TypeOrderUpdate.TRANS.value
    )
    await db.update_work_order(order_id=order_id, user_id=recip.user_id)
    order_info = await db.get_order(order_id=order_id)
    order_text = get_order_text(order_info)

    text = f'{user.name} передал вам заказ:\n\n{order_text}'
    await bot.send_message(
        chat_id=recip.user_id,
        text=text,
        reply_markup=kb.get_dlv_main_order_kb(
            order_id=order_info.id,
            order_status=order_info.g
        ))
    await cb.message.edit_text(
        text=f'{cb.message.text}\n\n✅ Заказ передан',
        entities=cb.message.entities,
        parse_mode=None
    )
    # журнал действий
    await db.save_user_action(
        user_id=cb.from_user.id,
        dlv_name=user.name,
        action=UserActions.TRANSFER_ORDER.value,
        comment=f'Получатель: {recip.name}')


# кнопка вернуть старую кб к заказу
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.BACK_MAIN_ORDER.value))
async def back_main_order(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    _, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)
    order_info = await db.get_order(order_id=order_id)
    await cb.message.edit_reply_markup(reply_markup=kb.get_dlv_main_order_kb(order_id, order_info.g))
