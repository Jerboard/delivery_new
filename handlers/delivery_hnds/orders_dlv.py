from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from datetime import datetime
from asyncio import sleep

import db
import keyboards as kb
from init import dp, bot, log_error
from config import Config
from utils import local_data_utils as dt
from utils.text_utils import get_order_text
from data.base_data import order_status_data, order_actions
from enums import (DeliveryCB, OrderStatus, DataKey, UserActions, DeliveryStatus, OrderAction, TypeOrderUpdate,
                   TypeOrderButton, KeyWords)


# кнопка взять заказ
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.ORDER_1.value))
async def dlv_order_1(cb: CallbackQuery):
    _, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    user_info = await db.get_user_info(cb.from_user.id)
    take_date = datetime.now(Config.tz).date().strftime(Config.day_form)

    # await db.add_work_order(user_id=cb.from_user.id, order_id=order_id)
    # добавить смену курьерской
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
        comment=f'{order_id}'
    )


# взять заказ на забор
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.TAKE_ORDER_2.value))
async def dlv_order_2(cb: CallbackQuery):
    _, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    order = await db.get_order(order_id)
    if not order:
        await cb.message.answer('❗️ОШИБКА. Что-то пошло не так - обратитесь к оператору')

    elif order.g != OrderStatus.NEW.value:
        await cb.message.answer ('❗️ОШИБКА. Заказ уже взял другой курьер')

    else:
        user_info = await db.get_user_info (cb.from_user.id)

        take_date = datetime.now (Config.tz).date ().strftime (Config.day_form)
        # await db.add_work_order(user_id=cb.from_user.id, order_id=order_id)
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
    _, order_id_str = cb.data.split(':')
    order_id = int(order_id_str)

    # if action == OrderAction.SUC.value:
    await cb.message.edit_reply_markup(reply_markup=kb.get_close_order_option_kb(order_id=order_id))

    # elif action == OrderAction.NOT_COME.value:
    #     await db.update_row_google(
    #         order_id=order_id,
    #         note=order_status_data.get(OrderStatus.NOT_COME.value)
    #     )
    #     await cb.message.edit_text(
    #         text=f'{cb.message.text}\n\n✖️ Клиент не явился',
    #         entities=cb.message.entities,
    #         parse_mode=None
    #     )

    # else:
        # await cb.answer('Нажмите кнопку "Подтвердить отказ", после этого заказ будет закрыт', show_alert=True)
        # await cb.message.edit_reply_markup(
        #     reply_markup=kb.get_close_order_kb(new_status_order=OrderStatus.REF.value, order_id=order_id))


# закрытие заказа буквы
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.ORDER_7.value))
async def dlv_order_7(cb: CallbackQuery):
    _, order_id_str, action = cb.data.split (':')
    order_id = int (order_id_str)

    await cb.message.edit_reply_markup(
        reply_markup=kb.get_done_order_letters_kb(order_id=order_id, order_action=action)
    )


# закрытие заказа
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.ORDER_4.value))
async def dlv_order_4(cb: CallbackQuery):
    _, order_id_str, order_action, lit = cb.data.split (':')
    order_id = int (order_id_str)

    if order_action == OrderAction.NOT_COME.value:
        await db.update_row_google (
            order_id=order_id,
            letter=KeyWords.NOT_COME.value,
            type_update=TypeOrderUpdate.STATE.value
        )
        order_info = await db.get_order (order_id)
        text = get_order_text(order_info)
        await cb.message.edit_text (text=text)
        return

    order_info = await db.get_order (order_id)
    await db.update_row_google (
        order_id=order_id,
        letter=lit,
        status=OrderStatus.SUC.value if order_info.g == OrderStatus.ACTIVE.value else OrderStatus.SUC_TAKE.value,
        type_update=TypeOrderUpdate.STATE.value
    )
    await cb.message.edit_text(
        text=f'{cb.message.text}\n\n✅Выполнен',
        entities=cb.message.entities,
        parse_mode=None
    )
    action = UserActions.SUCCESS_ORDER.value
    # if action == OrderStatus.SUC_TAKE.value:
    if order_info.g == OrderStatus.ACTIVE_TAKE.value:
        opr_info = await db.get_user_info (user_id=cb.from_user.id)
        text = f'✅Заказ получен курьером\n\n{cb.message.text}'
        await bot.send_message(opr_info.user_id, text)
        action = UserActions.SUCCESS_TAKE_ORDER.value

    # журнал действий
    await db.save_user_action (
        user_id=cb.from_user.id,
        dlv_name=order_info.f,
        action=action,
        comment=order_id_str)


# Закрытие заказа с изменениями. Запрос суммы изменений
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.ORDER_6.value))
async def edit_order_close_0(cb: CallbackQuery, state: FSMContext):
    _, action, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    await state.set_state(DeliveryStatus.EDIT_ORDER_CLOSE_1)
    # await state.update_data(data={'order_id': order_id, 'action': action})

    if action == OrderAction.COST.value:
        text = '📝 Введите сумму скидки'
    else:
        text = '📝 Введите фактическую стоимость доставки'

    await cb.message.edit_reply_markup(text, reply_markup=kb.get_back_close_order_kb(order_id))
    sent = await cb.message.answer(text)
    await state.update_data (data={'order_id': order_id, 'action': action, 'messages': [sent.message_id]})
    # await cb.message.answer(text, reply_markup=kb.get_close_kb())


# Закрытие заказа с изменениями. Запрос причины изменений
@dp.message(StateFilter(DeliveryStatus.EDIT_ORDER_CLOSE_1))
async def edit_order_close_1(msg: Message, state: FSMContext):

    if msg.text.isdigit():
        data = await state.get_data()

        if data['action'] == OrderAction.COST.value:
            await state.update_data(data={'discount': int(msg.text)})
        else:
            await state.update_data(data={'cost_dlv': int(msg.text)})

        await state.set_state(DeliveryStatus.EDIT_ORDER_CLOSE_2)

        sent = await msg.answer('Причина изменения стоимости')
        messages: list = data.get('messages', [])
        messages.append(msg.message_id)
        messages.append(sent.message_id)
        await state.update_data (data={'messages': messages})

    else:
        sent = await msg.answer('‼️Отправьте целое число')
        await sleep(3)
        await sent.delete()


# Закрытие заказа с изменениями. Закрытие
@dp.message(StateFilter(DeliveryStatus.EDIT_ORDER_CLOSE_2))
async def edit_order_close_2(msg: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    order_info = await db.get_order(order_id=data['order_id'])

    old_note = order_info.ab or ''
    amount = data.get('discount') or data.get('cost_dlv')
    note = f'{old_note}\n{order_actions.get(data["action"])} ({amount}) {msg.text}'.strip()
    if data ['action'] == OrderAction.COST.value:
        await db.update_row_google (
            order_id=data ['order_id'],
            type_update=data ['action'],
            discount=data ['discount'],
            note=note
        )
        user_action = UserActions.ADD_DISCOUNT.value
    else:
        await db.update_row_google (
            order_id=data ['order_id'],
            type_update=data ['action'],
            cost_delivery=data ['cost_dlv'],
            note=note
        )
        user_action = UserActions.ADD_DISCOUNT_DLV.value

    order_info = await db.get_order(data['order_id'])
    text = get_order_text(order_info)
    action = OrderAction.SUC_TAKE.value if order_info.g == OrderStatus.ACTIVE_TAKE.value else OrderAction.SUC.value
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
        type_update=TypeOrderUpdate.TRANS.value,
        letter='del'
    )
    # await db.update_work_order(order_id=order_id, user_id=recip.user_id)
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


# подтверждения забрать заказ у другого курьера
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.PICKUP_ORDER_1.value))
async def pickup_order_1(cb: CallbackQuery, state: FSMContext):
    _, order_id_str, action = cb.data.split(':')
    order_id = int(order_id_str)

    if action == 'back':
        order_info = await db.get_order(order_id=order_id)
        await cb.message.edit_reply_markup(reply_markup=kb.get_free_order_kb(
            order_id=order_id,
            type_order=TypeOrderButton.PICKUP.value,
            dlv_name=order_info.f
        ))
    else:
        await cb.message.edit_reply_markup(reply_markup=kb.get_pickup_order_kb(order_id))


# подтверждения забрать заказ у другого курьера
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.PICKUP_ORDER_2.value))
async def pickup_order_2(cb: CallbackQuery, state: FSMContext):
    _, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    order_info = await db.get_order (order_id=order_id)
    user_info = await db.get_user_info(user_id=cb.from_user.id)

    await db.update_row_google (
        order_id=order_id,
        dlv_name=user_info.name,
        type_update=TypeOrderUpdate.PICKUP.value
    )
    # order_text = get_order_text (order_info)
    text = f'{user_info.name} забрал заказ:\n\n{order_info.w} {order_info.x}'.replace('None', '')
    await bot.send_message (
        # chat_id=order_info.user_id,
        chat_id=524275902,
        text=text,
        reply_markup=kb.get_dlv_main_order_kb (
            order_id=order_info.id,
            order_status=order_info.g
        ))
    await cb.message.edit_reply_markup (reply_markup=kb.get_dlv_main_order_kb (order_id, order_info.g))



# кнопка вернуть старую кб к заказу
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.BACK_MAIN_ORDER.value))
async def back_main_order(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    _, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)
    order_info = await db.get_order(order_id=order_id)
    text = get_order_text (order_info)
    await cb.message.edit_text(text=text, reply_markup=kb.get_dlv_main_order_kb(order_id, order_info.g))


# возвращает к закрывающемуся заказу
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.BACK_CLOSE_ORDER.value))
async def back_close_order(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    _, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)
    order_info = await db.get_order(order_id=order_id)

    messages = data.get('messages', [])
    for message in messages:
        await bot.delete_message(chat_id=cb.message.chat.id, message_id=message)

    text = get_order_text (order_info)
    await cb.message.edit_text(text=text, reply_markup=kb.get_close_order_option_kb(order_id=order_id))
