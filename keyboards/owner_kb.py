from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from enums import OwnerCB


# клавиатура владельца на кнопке старт
def main_owner_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='➕🗂 Добавить/обновить заказы', callback_data=f'{OwnerCB.UPDATE_TABLE.value}:main')
    kb.button(text='➕🗂 Добавить/обновить отчёт', callback_data=f'{OwnerCB.UPDATE_TABLE.value}:report')
    kb.button(text='➕🚛 Добавить курьера', callback_data=f'{OwnerCB.ADD_USER_DLV.value}')
    kb.button(text='➕🧑‍💻 Добавить оператора', callback_data=f'{OwnerCB.ADD_USER_1.value}:opr')
    kb.button(text='➖🚛 Удалить курьера', callback_data=f'{OwnerCB.DEL_USER.value}:dlv')
    kb.button(text='➖🧑‍💻 Удалить оператора', callback_data=f'{OwnerCB.DEL_USER_1.value}:opr')
    kb.button(text='✉ Посмотреть заказы курьера', callback_data=f'{OwnerCB.SEND_MSG_1.value}')
    kb.button(text='📝 Сменить таблицу', callback_data=f'{OwnerCB.CHANGE_TAB.value}')
    kb.button(text='📋 Посмотреть заказы без курьера', callback_data=f'{OwnerCB.VIEW_FREE_ORDERS_1.value}:0:0:1')
    kb.button(text='📤 Выгрузить данные о курьерах', callback_data=f'{OwnerCB.UPDATE_USERS_TABLE_1.value}')
    kb.button(text='📥 Загрузить данные о курьерах', callback_data=f'{OwnerCB.UPDATE_USERS_TABLE_2.value}')
    return kb.adjust(1, 1, 2, 2, 2, 2, 1).as_markup()
