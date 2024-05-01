from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.enums.content_type import ContentType

from datetime import datetime
from asyncio import sleep

import db
import keyboards as kb
from init import dp, bot, TZ, log_error
from config import config
from .base_dlv import save_expenses
from utils.redis_utils import get_redis_data
from utils.text_utils import get_order_text
from data.base_data import order_status_data
from enums import DeliveryCB, OrderStatus, RedisKey, UserActions, DeliveryStatus, OrderAction, TypeOrderUpdate


# смена клавиатуры на клавиатуру с тратами
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.EXPENSES_DVL_1.value))
async def expenses_dvl_1(cb: CallbackQuery):
    await cb.message.edit_reply_markup(reply_markup=kb.expenses_dvl_kb())


# запрос подтверждения траты 1 Просит отправить сумму
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.EXPENSES_DVL_2.value))
async def expenses_dvl_2(cb: CallbackQuery, state: FSMContext):
    _, category_id = cb.data.split(':')
    await state.set_state(DeliveryStatus.EXPENSES_DVL_3)
    await state.update_data(data={'column': category_id})
    await cb.message.answer('Отправьте сумму расходов', reply_markup=kb.get_close_kb())


# запрос подтверждения траты 2 Подтверждает сумму просит фото
@dp.message(StateFilter(DeliveryStatus.EXPENSES_DVL_3))
async def expenses_dvl_3(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        data = await state.get_data()

        await state.update_data(data={data["column"]: int(msg.text), 'exp_sum': int(msg.text)})
        await state.set_state(DeliveryStatus.EXPENSES_DVL_4)

        if data['column'] in ['b', 'g', 'k']:
            text = f'Отправьте комментарий'
        else:
            text = f'Отправьте фото подтверждение траты и комментарий'
        await msg.answer(text, reply_markup=kb.get_close_kb())

    else:
        sent = await msg.answer('❗️ Отправьте сумму цифрой')
        await sleep(3)
        await sent.delete()


# запрос подтверждения траты 3 Принимает фото, если фото с текстом, то завершает процесс, если нет,
# то просит комментарий
@dp.message(StateFilter(DeliveryStatus.EXPENSES_DVL_4))
async def expenses_dvl_4(msg: Message, state: FSMContext):
    if msg.content_type == ContentType.PHOTO:
        await state.update_data(data={'photo_id': msg.photo[-1].file_id})
        if msg.caption:
            data = await state.get_data()
            await state.clear()
            await save_expenses(msg.from_user.id, data)

        else:
            await state.set_state(DeliveryStatus.EXPENSES_DVL_5)
            await msg.answer('Теперь отправьте комментарий', reply_markup=kb.get_close_kb())

    else:
        data = await state.get_data()
        if data ['column'] in ['b', 'g', 'k']:
            await state.clear()
            await save_expenses (msg.from_user.id, data)

        else:
            await msg.answer('Отправьте фото', reply_markup=kb.get_close_kb())


# сохраняет коммент
@dp.message(StateFilter(DeliveryStatus.EXPENSES_DVL_5))
async def expenses_dvl_5(msg: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    user_info = await db.get_user_info(user_id=msg.from_user.id)
    await save_expenses (msg.from_user.id, data)

    # expenses_dvl(msg.text, data['column'], data['sum'], dlv[6])

    today = datetime.now(TZ).strftime(config.time_form)
    text = f'Курьер: {user_info.name}\n' \
           f'Время: {today}\n' \
           f'Сумма: {data["sum"]} ₽\n' \
           f'Комментарий: {msg.text}'

    await bot.send_photo(config.group_expenses, photo=data['photo'], caption=text)
    await msg.answer('✅ Ваша трата учтена')
    # журнал действий
    await db.save_user_action (
        user_id=msg.from_user.id,
        dlv_name=user_info.name,
        action=UserActions.ADD_EXPENSES.value,
        comment=text
    )


# посмотреть траты за сегодня
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.EXPENSES_DVL_VIEW.value))
async def expenses_dvl_view(cb: CallbackQuery):
    user_info = await db.get_user_info(user_id=cb.from_user.id)
    expenses = await db.get_report_dlv(dlv_name=user_info.name)
    if not expenses:
        text = 'Нет трат'
    else:
        text = f'💸Траты за сегодня:\n\n{expenses.l}'
    await cb.message.answer(text)
