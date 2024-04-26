from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from datetime import datetime
from asyncio import sleep

import db
import keyboards as kb
from init import dp, bot, TZ, log_error
from config import config
from utils.redis_utils import get_redis_data
from utils.text_utils import get_order_text
from data.base_data import order_status_data
from enums import DeliveryCB, OrderStatus, RedisKey, UserActions, DeliveryStatus, OrderAction, TypeUpdate


# кнопка взять заказ
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.DLV_ORDER_1.value))
async def dlv_order_1(cb: CallbackQuery):
    _, row_num, order_id = map(int, cb.data.split(':')[1:])

    user_info = await db.get_user_info(cb.from_user.id)
    status = order_status_data.get (OrderStatus.ACTIVE.value)
    take_date = datetime.now(TZ).date().strftime(config.day_form)
    await db.update_row_google(
        order_id=order_id,
        dlv_name=user_info.name,
        status=status,
        take_date=take_date
    )
    await cb.message.edit_text(text=f'{cb.message.text}\n\n✅Принят')

    # журнал действий
    await db.save_user_action(
        user_id=cb.from_user.id,
        dlv_name=user_info.name,
        action=UserActions.TAKE_ORDER.value,
        comment=f'Строка {row_num}'
    )


# взять заказ на забор
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.TAKE_ORDER_2.value))
async def dlv_order_2(cb: CallbackQuery):
    _, row_num, order_id = map (int, cb.data.split (':') [1:])

    order = await db.get_order(order_id)
    if not order:
        await cb.message.answer('❗️ОШИБКА. Что-то пошло не так - обратитесь к оператору')

    elif order.g != OrderStatus.NEW.value:
        await cb.message.answer ('❗️ОШИБКА. Заказ уже взял другой курьер')

    else:
        user_info = await db.get_user_info (cb.from_user.id)
        status = order_status_data.get (OrderStatus.TAKE.value)
        take_date = datetime.now (TZ).date ().strftime (config.day_form)
        await db.update_row_google (
            order_id=order_id,
            dlv_name=user_info.name,
            status=status,
            take_date=take_date
        )

        sent_chats = get_redis_data(f'{RedisKey.ADD_OPR_ORDER.value}:{order_id}')
        for msg in sent_chats:
            try:
                await bot.delete_message(chat_id=msg['chat_id'], message_id=msg['message_id'])
            except:
                pass

        dlv_info = await db.get_user_info(user_id=cb.from_user.id)
        opr_info = await db.get_user_info(name=order.k)

        await cb.message.edit_text(text=f'{cb.message.text}\n\n✅ Принят')
        text = f'✅Заказ принят. {dlv_info.name}\n\n{cb.message.text}'
        await bot.send_message(opr_info.user_id, text)
        # журнал действий
        await db.save_user_action(
            user_id=cb.from_user.id,
            dlv_name=dlv_info.name,
            action=UserActions.TAKE_ORDER_TAKE.value,
            comment=order_id)


# Подтвердить доставку либо отмену заказа
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.DLV_ORDER_2.value))
async def dlv_order_2(cb: CallbackQuery):
    _, action, order_id_str = cb.data.split(':')
    order_id = int(order_id_str)

    if action == OrderAction.SUC.value:
        await cb.message.edit_reply_markup(reply_markup=kb.get_close_order_option_kb(order_id=order_id))

    elif action == OrderAction.NOT_COME.value:
        await db.update_row_google(order_id=order_id, note=OrderStatus.NOT_COME.value)
        await cb.message.edit_text(f'{cb.message.text}\n\n✖️ Клиент не явился')

    else:
        await cb.answer('Нажмите кнопку "Подтвердить отказ", после этого заказ будет закрыт', show_alert=True)
        await cb.message.edit_reply_markup(
            reply_markup=kb.get_close_order_kb(status_order=OrderStatus.REF.value, order_id=order_id))


# закрытие заказа
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.DLV_ORDER_4.value))
async def dlv_order_4(cb: CallbackQuery):
    _, order_status, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    order_info = await db.get_order (order_id)

    if order_status in [OrderStatus.SUC.value, OrderStatus.SUC_TAKE.value]:
        # тут буковку надо ещё добавить
        status_str = order_status_data.get (order_status)
        await db.update_row_google (
            order_id=order_id,
            status=status_str
        )
        await cb.message.edit_text(f'{cb.message.text} ✅Выполнен')

        action = UserActions.SUCCESS_ORDER.value
        if order_status == OrderStatus.SUC_TAKE.value:
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
        status_str = order_status_data.get (order_status)
        await db.update_row_google (
            order_id=order_id,
            status=status_str
        )
        await cb.message.edit_text(f'{cb.message.text} ✖️Отказ')

        # журнал действий
        await db.save_user_action(
            user_id=cb.from_user.id,
            dlv_name=order_info.f,
            action=UserActions.REFUSE_ORDER.value,
            comment=order_id_str)


# закрытие заказа с изминениями. Запрос суммы изминений
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.DLV_ORDER_6.value))
async def dlv_order_6(cb: CallbackQuery, state: FSMContext):
    _, action, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    await state.set_state(DeliveryStatus.EDIT_ORDER_CLOSE_1)
    await state.update_data(data={'order_id': order_id})

    if action == OrderAction.COST.value:
        await cb.message.answer('📝 Введите сумму скидки')
        await state.update_data(data={'action': 'cost'})
    else:
        await cb.message.answer('📝 Введите фактическую стоимость доставки')
        await state.update_data(data={'action': 'dlv'})


# закрытие заказа с изминениями. Запрос причины изминений
@dp.message(StateFilter(DeliveryStatus.EDIT_ORDER_CLOSE_1))
async def edit_order_close_1(msg: Message, state: FSMContext):

    if msg.text.isdigit():
        data = await state.get_data()

        if data['action'] == OrderAction.COST.value:
            await state.update_data(data={'discount': msg.text})
        else:
            await state.update_data(data={'cost': msg.text, 'discount': msg.text})

        await state.set_state(DeliveryStatus.EDIT_ORDER_CLOSE_2)
        sent = await msg.answer('Причина изменения стоимости')
        await state.update_data(data={'msg2': sent.message_id, 'msg3': msg.message_id})

    else:
        sent = await msg.answer('‼️Отправьте целое число')
        await sleep(3)
        await sent.delete()


# закрытие заказа с изменениями. закрытие
@dp.message(StateFilter(DeliveryStatus.EDIT_ORDER_CLOSE_2))
async def edit_order_close_2(msg: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    if data['action'] == OrderAction.COST.value:
        # row_to_temp_change_cost(data['row'], msg.text, data['discount'])
        await db.update_row_google(
            order_id=data['order_id'],
            type_update=TypeUpdate.EDIT_COST.value,
            discount=data['discount'],
            note=msg.text
        )
        # журнал действий
        action = UserActions.ADD_DISCOUNT.value
    else:
        # row_to_temp_change_dlv(data['row'], data['cost'], msg.text)
        # update_edit_cost(order_id, 'dlv', data['cost'], msg.text)
        await db.update_row_google (
            order_id=data ['order_id'],
            type_update=TypeUpdate.EDIT_COST_DELIVERY.value,
            discount=data ['discount'],
            note=msg.text
        )

        # журнал действий
        action = UserActions.ADD_DISCOUNT_DLV.value

    order_info = await db.get_order(data['order_id'])
    text = get_order_text(order_info)
    await msg.answer(text, reply_markup=kb.get_close_order_option_kb(data['order_id']))

    # журнал действий
    await db.save_user_action(
        user_id=msg.from_user.id,
        dlv_name=data['dlv_name'],
        action=action,
        comment=f'Строка {data["row"]}')


# кнопка передать заказ
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.DLV_ORDER_3.value))
async def dlv_order_3(cb: CallbackQuery):
    _, order_status, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    user_info = await db.get_user_info(cb.from_user.id)
    delivers = await db.get_users(exc_user_id=cb.from_user.id, company_id=user_info.company_id)

    await cb.message.edit_reply_markup(reply_markup=kb.get_transfer_order_kb(delivers, order_id))
    
    
# передаёт заказ
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.TRANS_ORDER.value))
async def trans_order(cb: CallbackQuery, state: FSMContext):
    _, user_id, order_id = map(int, cb.data.split(':')[1:])

    user = await db.get_user_info(cb.from_user.id)
    recip = await db.get_user_info(user_id)

    await db.update_row_google (order_id=order_id, dlv_name=recip.name)
    order_text = get_order_text(order_id)

    text = f'{user.name} передал вам заказ:\n\n{order_text}'
    await bot.send_message(recip.user_id, text)
    await cb.message.edit_text(f'{cb.message.text}\n\n✅ Заказ передан')
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
    await cb.message.edit_reply_markup(reply_markup=kb.get_dlv_main_order_kb(order_id))