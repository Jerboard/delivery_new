from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter, Command

import db
import keyboards as kb
from init import dp
from .delivery_hnds.base_dlv import delivery_start, get_profile_dlv
from .owner_hnds.owner_base import owner_start
from enums import UserStatus, DeliveryStatus, BaseCB


@dp.message(CommandStart())
async def com_start(msg: Message, state: FSMContext):
    print(msg.text)
    # await db.add_user (
    #     user_id=msg.from_user.id,
    #     full_name=msg.from_user.full_name,
    #     username=msg.from_user.username,
    #     status=UserStatus.OWN.value
    # )
    await state.clear()
    user_info = await db.get_user_info(msg.from_user.id)

    if len(msg.text) > 6:
        link = msg.text[-7:]
        check_link = await db.get_temp_link(link)
        if check_link:
            if not user_info:
                await db.add_user(
                    user_id=msg.from_user.id,
                    full_name=msg.from_user.full_name,
                    username=msg.from_user.username,
                    status=link[-3:]
                    )

            if link[-3:] == UserStatus.DLV.value:
                await state.set_state(DeliveryStatus.REG_NAME)
                await state.update_data(data={'comp_id': str(link).split('dlv')[1]})
                await msg.answer('Введите ваше имя')

            else:
                text = f'Для поиска заказов отправьте номер телефона, имя получателя или часть адреса'
                await msg.answer(text)

        else:
            await msg.answer('❌Ссылка не действительна')

    else:
        if not user_info:
            await msg.answer('❌ У вас нет доступа. Для получения доступа обратитесь к администратору')

        elif user_info.status == UserStatus.DLV.value:
            await delivery_start(user_id=msg.from_user.id, dlv_name=user_info.name)

        elif user_info.status == UserStatus.OPR.value:

            text = f'Для поиска заказов отправьте номер телефона, имя получателя или часть адреса'
            await msg.answer(text)

        elif user_info.status == UserStatus.OWN.value:
            await owner_start(msg.from_user.id)

        else:
            await msg.answer('❌ У вас нет доступа. Для получения доступа обратитесь к администратору')


# регистрирует имя
@dp.message(StateFilter(DeliveryStatus.REG_NAME))
async def reg_dlv_1(msg: Message, state: FSMContext):
    await state.update_data(data={'name': msg.text})

    data = await state.get_data()
    await state.clear()

    await db.update_user_info(user_id=msg.from_user.id, dlv_name=msg.text, company_id=data.get('comp_id'))
    text = f'Вы зарегистрированы. Для поиска заказов отправьте номер получателя или часть адреса сообщением'

    await msg.answer(text)


# Личный кабинет
@dp.message(Command('main'))
async def com_main(msg: Message, state: FSMContext):
    await state.clear()

    user_info = await db.get_user_info(msg.from_user.id)

    if user_info and user_info.status == UserStatus.DLV.value:
        await get_profile_dlv(user_id=msg.from_user.id, user_info=user_info)

    elif user_info and user_info.status in [UserStatus.OPR.value, UserStatus.OWN.value]:

        text = f'Оформить забор\n\nВыберите курьерскую'
        await msg.answer(text, reply_markup=kb.take_order_company_kb())

    else:
        await msg.answer('❌ У вас нет доступа. Для получения доступа обратитесь к администратору')


# отмена
@dp.callback_query(lambda cb: cb.data.startswith(BaseCB.CLOSE.value))
async def close(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.delete()
    await cb.answer('❌Отменено')
