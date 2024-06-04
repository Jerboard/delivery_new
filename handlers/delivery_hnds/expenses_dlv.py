from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.enums.content_type import ContentType

from datetime import datetime
from asyncio import sleep

import db
import keyboards as kb
from config import Config
from init import dp, bot
from .base_dlv import save_expenses
from data.base_data import expensis_dlv, letters
from enums import DeliveryCB, DeliveryStatus, UserActions


# смена клавиатуры на клавиатуру с тратами
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.EXPENSES_1.value))
async def expenses_dvl_1(cb: CallbackQuery):
    await cb.message.edit_reply_markup(reply_markup=kb.expenses_dvl_kb())


# запрос подтверждения траты 1 Просит отправить сумму
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.EXPENSES_2.value))
async def expenses_dvl_2(cb: CallbackQuery, state: FSMContext):
    _, ex_id_str = cb.data.split(':')
    ex_id = int(ex_id_str)

    await state.set_state(DeliveryStatus.EXPENSES_3)
    # await state.update_data(data={'column': category_id})
    await state.update_data(data={'ex_id': ex_id})
    await cb.message.answer('Отправьте сумму расходов', reply_markup=kb.get_close_kb())


# запрос подтверждения траты 2 Подтверждает сумму просит фото
@dp.message(StateFilter(DeliveryStatus.EXPENSES_3))
async def expenses_dvl_3(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        data = await state.get_data()
        ex_info = expensis_dlv[data['ex_id']]

        await state.update_data(data={ex_info['column']: int(msg.text), 'exp_sum': int(msg.text)})
        await state.set_state(DeliveryStatus.EXPENSES_4)

        if data['ex_id'] == 1:
            await msg.answer('Время работы: ', reply_markup=kb.get_expensis_let_kb())
            return
        elif ex_info['comment']:
            text = f'Отправьте комментарий'
        elif ex_info['photo']:
            text = f'Отправьте фото подтверждение траты'
        else:
            data = await state.get_data ()
            await state.clear()
            await save_expenses(msg.from_user.id, data)
            return
            # await state.update_data(data={'comment': ex_info['text']})

        await msg.answer(text, reply_markup=kb.get_close_kb())

    else:
        sent = await msg.answer('❗️ Отправьте сумму цифрой')
        await sleep(3)
        await sent.delete()


# запрос подтверждения траты 3 Принимает фото, если фото с текстом, то завершает процесс, если нет,
# то просит комментарий
@dp.message(StateFilter(DeliveryStatus.EXPENSES_4))
async def expenses_dvl_4(msg: Message, state: FSMContext):
    if msg.content_type == ContentType.PHOTO:
        await state.update_data(data={'photo_id': msg.photo[-1].file_id})

        data = await state.get_data ()
        await state.clear ()
        await save_expenses (msg.from_user.id, data)
    else:
        await state.update_data (data={'comment': msg.text})
        data = await state.get_data()
        await state.clear()
        await save_expenses (msg.from_user.id, data)


# сохраняем зп
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.EXPENSES_5.value))
async def expenses_dvl_5(cb: CallbackQuery, state: FSMContext):
    _, letter = cb.data.split(':')

    data = await state.get_data ()
    # await cb.message.edit_reply_markup(reply_markup=None)
    ex_info = expensis_dlv [data ['ex_id']]
    data['comment'] = f'{ex_info["text"]} {letters[letter]}'
    await state.clear ()
    await save_expenses (cb.from_user.id, data)
    await cb.message.delete ()


# посмотреть траты за сегодня
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.EXPENSES_VIEW.value))
async def expenses_dvl_view(cb: CallbackQuery):
    user_info = await db.get_user_info(user_id=cb.from_user.id)
    expenses = await db.get_report_dlv(dlv_name=user_info.name)
    if not expenses:
        text = 'Нет трат'
    else:
        expenses_str = '\n'.join(expenses.l)
        text = f'💸Траты за сегодня:\n\n{expenses_str}'
    await cb.message.answer(text)
