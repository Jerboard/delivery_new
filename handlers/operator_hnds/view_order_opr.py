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


# выбор даты заказа
@dp.callback_query(lambda cb: cb.data.startswith(OperatorCB.VIEW_ORDER_1.value))
async def take_order_1(cb: CallbackQuery, state: FSMContext):
    _, order_status = cb.data.split (':')