from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from datetime import datetime
from asyncio import sleep

import db
import keyboards as kb
from init import dp, bot, log_error
from config import Config
from utils import local_data_utils as dt
from utils.text_utils import get_order_text
from data.base_data import order_status_data, order_actions
from enums import (DeliveryCB, OrderStatus, DataKey, UserActions, DeliveryStatus, OrderAction, TypeOrderUpdate,
                   TypeOrderButton)


# старт почтовых курьеров
async def post_order_main(user_id: int, order_id: int, msg_id: int = 0, user_info: db.UserRow = None) -> None:
    pass

