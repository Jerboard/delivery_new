from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

import db
from data.base_data import expensis_dlv
from enums import DeliveryCB, OrderAction, OrderStatus


# клавиатура ЛК курьера
def main_dvl_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🖌 Сменить имя', callback_data=DeliveryCB.EDIT_DLV_NAME.value)
    kb.button(text='📝 Отчёт', callback_data=DeliveryCB.REPORT_DVL_1.value)
    kb.button(text='💸 Траты', callback_data=DeliveryCB.EXPENSES_DVL_1.value)
    kb.button(text='💸 Посмотреть траты за сегодня', callback_data=DeliveryCB.EXPENSES_DVL_VIEW.value)
    return kb.adjust(2).as_markup()


# клава для курьера свободный заказ
def get_free_order_kb(order_id: int, order_status: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if order_status == OrderStatus.NEW.value:
        kb.button(text='📦 Взять в работу', callback_data=f'{DeliveryCB.DLV_ORDER_1.value}:{order_id}')
    else:
        kb.button(text='📦 Взять в работу', callback_data=f'{DeliveryCB.TAKE_ORDER_2.value}:{order_id}')
    return kb.adjust (1).as_markup ()


# клава для курьера свободное сообщение
def get_dlv_main_order_kb(order_id: int, order_status: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if order_status == OrderStatus.ACTIVE.value:
        kb.button(text='✅ Доставлен', callback_data=f'{DeliveryCB.DLV_ORDER_2.value}:{OrderAction.SUC.value}:{order_id}')
    else:
        kb.button(text='✅ Забрал', callback_data=f'{DeliveryCB.DLV_ORDER_4.value}:{OrderAction.SUC.value}:{order_id}')

    kb.button(text='❌ Отказ', callback_data=f'{DeliveryCB.DLV_ORDER_2.value}:{OrderAction.REF.value}:{order_id}')

    if order_status == OrderStatus.ACTIVE.value:
        kb.button(
            text='✖️ Клиент не явился',
            callback_data=f'{DeliveryCB.DLV_ORDER_2.value}:{OrderStatus.NOT_COME.value}:{order_id}')
    kb.button(text='↩️ Передать другому курьеру', callback_data=f'{DeliveryCB.DLV_ORDER_3.value}:{order_id}')
    return kb.adjust(1).as_markup()


# основная клавиатура закрытия заказа
def get_close_order_option_kb(order_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='✅ Закрыть заказ',
        callback_data=f'{DeliveryCB.DLV_ORDER_4.value}:{OrderAction.SUC.value}:{order_id}')
    kb.button(
        text='🖍 Изменить стоимость',
        callback_data=f'{DeliveryCB.DLV_ORDER_6.value}:{OrderAction.COST.value}:{order_id}')
    kb.button(
        text='🖍 Изменить цену доставки',
        callback_data=f'{DeliveryCB.DLV_ORDER_6.value}:{OrderAction.DELI.value}:{order_id}')
    kb.button(text='❌ Отмена', callback_data=f'{DeliveryCB.BACK_MAIN_ORDER.value}:{order_id}')
    return kb.adjust(1).as_markup()


# кнопка подтвердить Отказа от заказа
def get_close_order_kb(status_order: str, order_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='✅ Подтвердить отказ', callback_data=f'{DeliveryCB.DLV_ORDER_4.value}:{status_order}:{order_id}')
    kb.button(text='🔙 Назад', callback_data=f'{DeliveryCB.BACK_MAIN_ORDER.value}:{order_id}')
    return kb.adjust(1).as_markup()


# передать заказ
def get_transfer_order_kb(users: tuple[db.UserRow], order_id) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Назад', callback_data=f'{DeliveryCB.BACK_MAIN_ORDER.value}:{order_id}')
    for user in users:
        kb.button(text=user.name, callback_data=f'{DeliveryCB.TRANS_ORDER.value}:{user.user_id}:{order_id}')

    return kb.adjust(1, 2).as_markup()


# клавиатура трат курьера
def expenses_dvl_kb(is_report=0, cb_1=0, cb_2=0) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if is_report == 0:
        kb.button(text='🔙 Назад', callback_data=DeliveryCB.BACK_DLV_MAIN.value)
    else:
        kb.button(text='🔙 Назад', callback_data=f'{DeliveryCB.REPORT_DVL_1.value}:{cb_1}:{cb_2}')

    for column, name in expensis_dlv.items():
        kb.button(text=f'💸 {name}', callback_data=f'{DeliveryCB.EXPENSES_DVL_2.value}:{column}')

    return kb.adjust(1, 2).as_markup()


# дни просмотра отчёта
def report_view_days_kb(report_rows: tuple[db.ReportRow]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Сегодня', callback_data=f'{DeliveryCB.REPORT_DVL_2.value}:today')
    kb.button(text='🔙 Назад', callback_data=f'{DeliveryCB.BACK_DLV_MAIN.value}')

    for day_row in report_rows:
        kb.button(text=day_row.m, callback_data=f'{DeliveryCB.REPORT_DVL_2.value}:{day_row.m}')
    return kb.adjust(2).as_markup()


# отправить отчёт
def get_day_report_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    kb.button (text='📤 Отправить отчёт', callback_data=f'{DeliveryCB.REPORT_DVL_4.value}')
    kb.button (text='💸 Внести трату', callback_data=f'{DeliveryCB.EXPENSES_DVL_1.value}')
    return kb.adjust(1).as_markup()


# отправить отчёт
def get_send_day_report_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='📤 Отправить отчёт', callback_data=DeliveryCB.REPORT_DVL_3.value)
    return kb.adjust(1).as_markup()
