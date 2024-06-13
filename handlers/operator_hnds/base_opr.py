from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime

import db
import keyboards as kb
from init import dp, bot, log_error
from config import Config
from utils import text_utils as txt
from utils.base_utils import get_today_date_str
from data.base_data import company_dlv, order_status_data, work_chats
from enums import OperatorCB, OperatorStatus, TypeOrderUpdate, OrderStatus, DataKey, UserActions, UserRole, TypeOrderButton


# основное меню оператора
async def get_profile_opr(user_id: int, user_info: db.UserRow = None, msg_id: int = None):
    if not user_info:
        user_info = await db.get_user_info (user_id)

    orders = await db.get_orders_statistic (opr_name=user_info.name)
    statistic_text = txt.get_statistic_text (orders)
    text = f'{user_info.name}\n\n{statistic_text}'

    if msg_id:
        await bot.edit_message_text (text, reply_markup=kb.get_main_opr_kb (), chat_id=user_id, message_id=msg_id)
    else:
        await bot.send_message (user_id, text, reply_markup=kb.get_main_opr_kb ())
