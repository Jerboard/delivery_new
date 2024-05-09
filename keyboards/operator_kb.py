from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

import db
from data.base_data import company
from enums import BaseCB, OperatorCB, OrderStatus, TypeOrderUpdate


# курьерская для забора
def take_order_company_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for comp_id, name in company.items():
        kb.button(text=name, callback_data=f'{OperatorCB.TAKE_ORDER_1.value}:{comp_id}')

    return kb.adjust(1).as_markup()


# курьерская для забора
def get_take_order_kb(with_confirm: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='❌ Отмена', callback_data=BaseCB.CLOSE.value)
    if with_confirm:
        kb.button(text='✅ Подтвердить', callback_data=OperatorCB.TAKE_ORDER_2.value)
    return kb.as_markup()
