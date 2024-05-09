from enum import Enum


class UserRole(str, Enum):
    DLV = 'dlv'
    OPR = 'opr'
    OWN = 'own'


class OrderStatus(str, Enum):
    NEW = 'new'
    SUC = 'success'
    ACTIVE = 'active'
    ACTIVE_TAKE = 'active_take'
    REF = 'refuse'
    TAKE = 'take'
    SUC_TAKE = 'success_take'
    REF_TAKE = 'refuse_take'
    NOT_COME = 'not_come'
    REMAKE = 'remake'
    SEND = 'send'


class OrderAction(str, Enum):
    SUC = 'success'
    NOT_COME = 'not_come'
    REF = 'refuse'
    TRANS = 'trans'
    COST = 'edit_cost'
    DELI = 'edit_cost_dlv'


class DataKey(str, Enum):
    ADD_OPR_ORDER = 'add_opr_order'
    ORDERS = 'dlv_orders'


class UserActions(str, Enum):
    TAKE_ORDER = 'Взял заказ'
    TAKE_ORDER_TAKE = 'Взял заказ (забор)'
    REFUSE_ORDER = 'Отказался от заказа'
    SUCCESS_ORDER = 'Заказ выполнен'
    REFUSE_TAKE_ORDER = 'Отказался от забора'
    SUCCESS_TAKE_ORDER = 'Забор выполнен'
    NOT_COME_ORDER = 'Клиент не вышел'
    ADD_DISCOUNT = 'Добавил скидку'
    ADD_DISCOUNT_DLV = 'Изменил стоимость доставки'
    TRANSFER_ORDER = 'Передал заказ'
    ADD_EXPENSES = 'Добавил трату'
    VIEW_REPORT = 'Просмотрел отчёт'
    SEND_REPORT = 'Отправил отчёт'


class TypeOrderUpdate(str, Enum):
    EDIT = 'edit'
    ADD = 'add'
    ADD_OPR = 'add_opr'
    STATE = 'state'
    EDIT_COST = 'edit_cost'
    EDIT_COST_DELIVERY = 'edit_cost_dlv'
    NOT_COME = 'not_come'
    UP_DATE = 'up_date'
    TRANS = 'trans'


class SearchType(str, Enum):
    PHONE = 'phone'
    NAME = 'name'
    METRO = 'metro'


class ShortText (str, Enum):
    ACTIVE = 'active_orders'
    FREE = 'free_orders'


class CompanyDLV (str, Enum):
    POST = 'post'
    MASTER = 'master'
    PUTILIN = 'putilin'
    MASTER_SPB = 'master_spb'
