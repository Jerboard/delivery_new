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
from utils.base_utils import get_random_code
from data.base_data import order_status_data
from enums import OwnerCB, UserRole, RedisKey, UserActions, OwnerStatus, OrderAction, TypeUpdate


# меняет рабочую таблицу. Запрашивает номер новой таблицы
@dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.ADD_USER_1.value))
async def add_user_1(cb: CallbackQuery, state: FSMContext):
    await cb.message.edit_reply_markup(reply_markup=kb.get_add_dlv_comp_kb())


@dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.ADD_USER_2.value))
async def add_user_1(cb: CallbackQuery, state: FSMContext):
    _, role, comp_id = cb.data.split(':')
    code_verif = get_random_code()

    link = f'https://t.me/{config.bot_name}?start={comp_id}-{code_verif}-{role}'

    await db.add_temp_link(code_verif)
    text = f'Для начала работы перейдите по ссылке и пройдите простую регистрацию\n\n' \
           f'{link}'

    await cb.message.answer(text)

