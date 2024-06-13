from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

import db
from data.base_data import company_dlv
from enums import BaseCB, OperatorCB, UserRole, OwnerCB, OrderStatus


# основная клавиатура оператора
def get_main_opr_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button (text='⚪️ Без статуса', callback_data=f'{OperatorCB.VIEW_ORDER_1.value}:{OrderStatus.NEW.value}')
    kb.button (text='🟢 Доставлен', callback_data=f'{OperatorCB.VIEW_ORDER_1.value}:{OrderStatus.SUC.value}')
    kb.button (text='🟠 Отправлен', callback_data=f'{OperatorCB.VIEW_ORDER_1.value}:{OrderStatus.SEND.value}')
    kb.button (text='🟡 На руках', callback_data=f'{OperatorCB.VIEW_ORDER_1.value}:{OrderStatus.ACTIVE.value}')
    kb.button (text='🔴 Отказ', callback_data=f'{OperatorCB.VIEW_ORDER_1.value}:{OrderStatus.REF.value}')
    kb.button (text='🔵 Оформить забор', callback_data=f'in_dev')
    return kb.adjust (2).as_markup ()


# курьерская для забора
def take_order_company_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for comp_id, name in company_dlv.items():
        kb.button(text=name, callback_data=f'{OperatorCB.TAKE_ORDER_1.value}:{comp_id}')

    return kb.adjust(1).as_markup()


# курьерская для забора
def get_take_order_kb(role: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='❌ Отмена', callback_data=BaseCB.CLOSE.value)
    if role == UserRole.OPR.value:
        kb.button(text='✅ Подтвердить', callback_data=OperatorCB.TAKE_ORDER_2.value)
    elif role == UserRole.OWN.value:
        kb.button(text='✅ Подтвердить', callback_data=OwnerCB.ADD_ORDER.value)
    return kb.as_markup()
