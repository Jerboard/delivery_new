from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

import db
import keyboards as kb
from init import dp
from .base_dlv import get_profile_dlv
from enums import DeliveryCB, DeliveryStatus


# возвращает в лк курьера
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.BACK_MAIN.value))
async def expenses_dvl_0(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await get_profile_dlv(cb.from_user.id, msg_id=cb.message.message_id)


# смена имени курьера запрос имени
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.EDIT_NAME.value))
async def edit_dlv_name(cb: CallbackQuery, state: FSMContext):
    user_info = await db.get_user_info(cb.from_user.id)

    text = f'Ваше имя: {user_info.name}\n' \
           f'Введите новое имя\n' \
           f'Для отмены нажмите старт/start\n\n' \
           f'❗️Ваше имя будет отображаться в таблице администратора'

    await state.set_state(DeliveryStatus.EDIT_NAME)
    await state.update_data(data={'msg_id': cb.message.message_id})
    await cb.message.edit_text(text, reply_markup=kb.get_main_dlv_menu_kb())


# смена имени курьера сохранение
@dp.message(StateFilter(DeliveryStatus.EDIT_NAME))
async def com_start(msg: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await msg.delete()

    await db.update_user_info(user_id=msg.from_user.id, name=msg.text)

    await get_profile_dlv (user_id=msg.from_user.id, msg_id=data['msg_id'])
