from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from datetime import datetime
from asyncio import sleep

import db
import keyboards as kb
from init import dp, bot, TZ, log_error
from config import config
from google_api.utils_google import is_table_exist
from google_api.base_google import save_new_order_table, save_new_report_table
from utils.json_utils import save_json_data
from utils.text_utils import get_order_text
from data.base_data import order_status_data
from enums import OwnerCB, OrderStatus, RedisKey, UserActions, OwnerStatus, OrderAction, TypeOrderUpdate


# меняет рабочую таблицу. Запрашивает номер новой таблицы
@dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.CHANGE_TAB.value))
async def change_tab_1(cb: CallbackQuery, state: FSMContext):
    await state.set_state(OwnerStatus.CHANGE_TAB)
    text = f'Отправьте номер новой таблицы.\n\n' \
           f'‼️Важно: рабочая таблица должна располагаться на первом листе. ' \
           f'Не забудьте дать боту доступ к таблице\n\n' \
           f'Служебный аккаунт:\n\n <code>servise-test@my-project-sheet-test-130722.iam.gserviceaccount.com</code>'

    await cb.message.answer(text, reply_markup=kb.get_close_kb())


# меняет рабочую таблицу. Проверяет таблицу
@dp.message(StateFilter(OwnerStatus.CHANGE_TAB))
async def change_tab_2(msg: Message, state: FSMContext):
    await state.clear()
    time_start = datetime.now()
    sent = await msg.answer ('⏳ Таблица обновляется это может занять какое-то время')

    if is_table_exist(msg.text):
        update_table = False
        while update_table:
            wait_orders = await db.get_orders (get_wait_update=True)
            wait_reports = await db.get_reports_all_dlv (get_wait_update=True)

            wait_updates = wait_orders + wait_reports
            if wait_updates == 0:
                update_table = True
            else:
                await sent.edit_text (f'⏳ Ожидает внесения изменений. Примерно {wait_updates * 3} с.')
                await sleep(3)

        # очистить таблицу
        await db.delete_orders ()
        # обновляет таблицу
        await save_new_order_table()
        # очистить таблицу отчётов
        await db.clear_report_table ()
        # обновляет отчёт и траты
        await save_new_report_table()
        # сохраняет новую таблицу
        save_json_data(data={'tab_id': msg.text}, file_name=config.table_file)
        time_finish = datetime.now() - time_start
        await sent.edit_text(f'✅ Таблица обновлена\nВремя обновления: {time_finish}')

    else:
        await sent.delete()
        await msg.answer('‼ Произошла ошибка. Неправильный номер таблицы или ошибка доступа')
