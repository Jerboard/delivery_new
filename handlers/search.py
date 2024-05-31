from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.enums.chat_type import ChatType

import db
import keyboards as kb
from init import dp, log_error
from utils import text_utils as txt
from enums import UserRole, SearchType, OrderStatus


# поиск заказов
@dp.message(StateFilter(default_state))
async def search(msg: Message):
    if msg.chat.type != ChatType.PRIVATE:
        return

    user_info = await db.get_user_info(msg.from_user.id)
    if not user_info:
        await msg.answer('❌ У вас нет доступа. Для получения доступа обратитесь к администратору')

    elif len(msg.text) >= 1:
        query = msg.text.lower()
        search_on = SearchType.PHONE if query.isdigit() else SearchType.METRO
        # comp = user_info.company if user_info.role == UserRole.DLV.value else None

        orders = await db.get_orders (search_query=query, search_on=search_on)
        if not orders:
            orders = await db.get_orders (search_query=query, search_on=SearchType.NAME)

        if not orders:
            await msg.answer ('❌ По вашему запросу ничего не найдено')
            return

        if user_info.role == UserRole.DLV.value:
            counter = 0
            for order in orders:
                print(order)
                try:
                    text = txt.get_order_text(order)
                    if order.f == user_info.name and order.g in [OrderStatus.ACTIVE.value, OrderStatus.ACTIVE_TAKE.value]:
                        counter += 1
                        await msg.answer(text, reply_markup=kb.get_dlv_main_order_kb(
                            order_id=order.id,
                            order_status=order.g
                        ))

                    # elif order.g in [OrderStatus.NEW.value, OrderStatus.TAKE.value]:
                    elif order.g == OrderStatus.NEW.value:
                        counter += 1
                        await msg.answer(text, reply_markup=kb.get_free_order_kb(order_id=order.id))
                except Exception as ex:
                    log_error(ex)

            if counter == 0:
                await msg.answer('❌ По вашему запросу ничего не найдено')

        elif user_info.role in [UserRole.OPR.value, UserRole.OWN.value]:
            if len(orders) <= 3:
                for order in orders:
                    text = txt.get_admin_order_text(order)

                    keyboard = None
                    if user_info.role == UserRole.OWN.value:
                        if order.g in [OrderStatus.ACTIVE.value, OrderStatus.ACTIVE_TAKE.value]:
                            keyboard = kb.get_busy_order_own_kb (order_id=order.id)

                        elif order.g == OrderStatus.NEW.value:
                            keyboard = kb.get_free_order_own_kb(order_id=order.id)

                        else:
                            keyboard = kb.get_close_order_own_kb(
                                order_id=order.id,
                                dlv_name=order.f,
                                user_id=order.user_id
                            )
                    await msg.answer(text, reply_markup=keyboard)

            elif len(orders) > 30:
                await msg.answer(f'❗️По вашему запросу найдено {len(orders)}. Задайте более чёткие критерии поиска')

            else:
                orders_text = ''
                spt = '---------------------------\n'
                for order in orders:
                    short_order = txt.get_short_order_row(order, for_=user_info.role)
                    orders_text = f'{orders_text}{short_order}{spt}'

                text = f'Заказы ({len(orders)}):\n' \
                       f'{orders_text}'

                await msg.answer(text)

    else:
        await msg.answer('❗️Запрос должен быть не меньше 5и символов')
