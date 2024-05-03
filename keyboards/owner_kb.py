from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from data.base_data import company
from enums import OwnerCB, UserRole


# клавиатура владельца на кнопке старт
def main_owner_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='📄 Добавить/Обновить заказы', callback_data=f'{OwnerCB.UPDATE_TABLE.value}:order')
    kb.button(text='📄 Добавить/Обновить отчеты', callback_data=f'{OwnerCB.UPDATE_TABLE.value}:report')
    kb.button(text='🏃 Добавить Курьера', callback_data=f'{OwnerCB.ADD_USER_1.value}:{UserRole.DLV.value}')
    kb.button(text='🧑‍💻 Добавить Оператора', callback_data=f'{OwnerCB.ADD_USER_2.value}:{UserRole.OPR.value}:0')
    kb.button(text='🏃‍♂️ Удалить Курьера', callback_data=f'{OwnerCB.DEL_USER.value}:{UserRole.DLV.value}')
    kb.button(text='🙅 Удалить Оператора', callback_data=f'{OwnerCB.DEL_USER_1.value}:{UserRole.OPR.value}')
    kb.button(text='🗒 У Курьера', callback_data=f'{OwnerCB.SEND_MSG_1.value}')
    kb.button(text='📝 Сменить таблицу', callback_data=f'{OwnerCB.CHANGE_TAB.value}')
    kb.button(text='🗒 Без Курьера', callback_data=f'{OwnerCB.VIEW_FREE_ORDERS_1.value}:0:0:1')
    kb.button(text='📤 Выгрузить данные', callback_data=f'{OwnerCB.UPDATE_USERS_TABLE_1.value}')
    kb.button(text='📥 Загрузить данные', callback_data=f'{OwnerCB.UPDATE_USERS_TABLE_2.value}')
    return kb.adjust(1, 1, 2, 2, 2, 2, 1).as_markup()


# список курьерских для добавления курьера
def get_add_dlv_comp_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Назад', callback_data=OwnerCB.BACK.value)
    for k, v in company.items():
        kb.button(text=v, callback_data=f'{OwnerCB.ADD_USER_2.value}:{UserRole.DLV.value}:{k}')

    return kb.adjust(1, 2).as_markup()


# Владелец для заказов на руках
def get_busy_order_own_kb(order_id: int, dlv_name: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Снять', callback_data=f'{OwnerCB.MAKE_ORDER_EMPTY}:{order_id}:{dlv_name}')
    kb.button(text='Передать', callback_data=f'{OwnerCB.TRANS_ORDER_1}:{order_id}:{dlv_name}')
    return kb.adjust(2).as_markup()


# кнопка назначить заказ заказа
def get_free_order_own_kb(order_id: int, dlv_name: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    kb.button (text='Назначить', callback_data=f'{OwnerCB.TRANS_ORDER_1}:{order_id}:{dlv_name}')
    return kb.as_markup ()


# вернуть заказ курьеру
def get_close_order_own_kb(order_id: int, dlv_name: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    kb.button (
        text=f'↪️ Вернуть курьеру {dlv_name}',
        callback_data=f'{OwnerCB.TRANS_ORDER_2.value}:{order_id}:{dlv_name}')
    return kb.as_markup ()
