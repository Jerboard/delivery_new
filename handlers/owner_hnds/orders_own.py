from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from datetime import datetime
import re
import db
import keyboards as kb
from init import dp, bot, log_error
from config import Config
from utils import text_utils as txt
from enums import OwnerCB, UserRole, OrderStatus, OwnerStatus, UserActions, TypeOrderUpdate


# принимает заказ на забор
async def add_new_order(user_id: int, state: FSMContext):
    text = ('Чтобы отправить новый заказ - подставьте данные в форму \n\n'
            '<code>Исполнитель: \n'
            'Выдан: \n'
            'Принят: \n'
            'Оператор: \n'
            'Партнер: \n'
            'ФИО: \n'
            'Номер: \n'
            'Доп.номер: \n'
            'Бланк: \n'
            'Цена: \n'
            'Наценка: \n'
            'Доп: \n'
            'Биток: \n'
            'Доставка: \n'
            'Кошелек: \n'
            'Карта: \n'
            'Метро: \n'
            'Адрес: \n'
            'Цена бланка: \n'
            'Примечание: \n</code>')

    await state.set_state(OwnerStatus.ADD_ORDER)
    sent = await bot.send_message(chat_id=user_id, text=text, reply_markup=kb.get_close_kb())
    await state.update_data(data={'msg_id': sent.message_id})


# просмотр заказа
@dp.message (StateFilter(OwnerStatus.ADD_ORDER))
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
@dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.ADD_ORDER.value))
async def take_order_2(cb: CallbackQuery, state: FSMContext):
    sent_wait = await cb.message.answer ('⏳')
    await state.clear ()

    last_row = await db.get_max_row_num ()
    data_text = cb.message.text.split ('\n')
    await db.add_row(
        row_num=last_row + 1,
        g=OrderStatus.NEW.value,
        h=data_text[0].replace('Исполнитель:', '').strip(),
        i=data_text[1].replace('Выдан:', '').strip(),
        j=data_text[2].replace('Принят:', '').strip(),
        k=data_text[3].replace('Оператор:', '').strip(),
        l=data_text[4].replace('Партнер:', '').strip(),
        m=data_text[5].replace('ФИО:', '').strip(),
        n=re.sub (r'\D+', '', data_text[6]),
        o=re.sub (r'\D+', '', data_text[7]),
        p=data_text[8].replace('Бланк:', '').strip(),
        q=int(re.sub (r'\D+', '', data_text[9])),
        r=int(re.sub (r'\D+', '', data_text[10])),
        s=int(re.sub (r'\D+', '', data_text[11])),
        b=data_text[12].replace('Биток:', '').strip(),
        t=int(re.sub (r'\D+', '', data_text[13])),
        u=int(re.sub (r'\D+', '', data_text[14])),
        v=int(re.sub (r'\D+', '', data_text[15])),
        w=data_text[16].replace('Метро:', '').strip(),
        x=data_text[17].replace('Адрес:', '').strip(),
        z=data_text[18].replace('Цена бланка:', '').strip(),
        ab=data_text[19].replace('Примечание:', '').strip(),
        type_update=TypeOrderUpdate.ADD.value
    )

    text = f'✅Заявка добавлена.\n\n{cb.message.text}'
    await sent_wait.edit_text(text)


# передать заказ курьеру. Список курьеров
@dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.TRANS_ORDER_1.value))
async def trans_order_1(cb: CallbackQuery):
    _, order_id_str = cb.data.split(':')
    order_id = int(order_id_str)
    dlvs = await db.get_users(role=UserRole.DLV.value)

    await cb.message.edit_reply_markup(reply_markup=kb.get_trans_orders_users_kb(users=dlvs, order_id=order_id))


# передать заказ курьеру. Передаёт заказ
@dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.TRANS_ORDER_2.value))
async def trans_order_2(cb: CallbackQuery):
    # user_id, order_id = map(int, cb.data.split(':')[1:])
    _, user_id_str, order_id_str = cb.data.split(':')
    user_id = int(user_id_str)
    order_id = int(order_id_str)

    user_info = await db.get_user_info (user_id=user_id)
    take_date = datetime.now (Config.tz).date ().strftime (Config.day_form)

    # await db.add_work_order (user_id=user_info.user_id, order_id=order_id)
    await db.update_row_google (
        order_id=order_id,
        dlv_name=user_info.name,
        status=OrderStatus.ACTIVE.value,
        take_date=take_date,
        type_update=TypeOrderUpdate.STATE.value
    )

    order_info = await db.get_order(order_id=order_id)
    dlv_text = txt.get_order_text (order_info)
    text = f'❗️ Вам назначен заказ\n\n{dlv_text}'
    await bot.send_message(chat_id=user_id, text=text, reply_markup=kb.get_dlv_main_order_kb(
        order_id=order_id,
        order_status=OrderStatus.ACTIVE.value
    ))

    new_text = txt.get_admin_order_text (order_info)
    await cb.message.edit_text(
        text=new_text,
        reply_markup=kb.get_busy_order_own_kb (order_id=order_id)
    )
    await db.save_user_action(
        user_id=cb.from_user.id,
        dlv_name=user_info.name,
        action=UserActions.TRANSFER_ORDER_OWN.value,
        comment=str(order_id)
    )


# делает заказ свободным
@dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.MAKE_ORDER_FREE.value))
async def back_free(cb: CallbackQuery):
    _, order_id_str = cb.data.split(':')
    order_id = int(order_id_str)

    # await db.delete_work_order (order_id=order_id)
    await db.update_row_google (
        order_id=order_id,
        dlv_name='-',
        status=OrderStatus.NEW.value,
        take_date=' ',
        letter='del',
        type_update=TypeOrderUpdate.STATE.value
    )

    order_info = await db.get_order(order_id=order_id)
    text = txt.get_admin_order_text (order_info)
    await cb.message.edit_text (text=text, reply_markup=kb.get_free_order_own_kb (order_id=order_id))


# возвращает фри клаву заказу
@dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.BACK_FREE.value))
async def back_free(cb: CallbackQuery):
    _, order_id_str = cb.data.split(':')
    order_id = int(order_id_str)

    await cb.message.edit_reply_markup(reply_markup=kb.get_free_order_own_kb(order_id=order_id))
