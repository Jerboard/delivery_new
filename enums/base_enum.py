from enum import Enum


class UserStatus(str, Enum):
    DLV = 'dlv'
    OPR = 'opr'
    OWN = 'own'


class OrderStatus(str, Enum):
    NEW = '-'
    SUC = 'success'
    ACTIVE = 'active'
    # ACTIVE_TAKE = 'active_take'
    REF = 'refuse'
    TAKE = 'take'
    SUC_TAKE = 'success_take'
    REF_TAKE = 'refuse_take'
    NOT_COME = 'not_come'


class OrderAction(str, Enum):
    SUC = 'success'
    NOT_COME = 'not_come'
    REF = 'refuse'
    COST = 'edit_cost'
    DELI = 'edit_delivery'


class RedisKey(str, Enum):
    ADD_OPR_ORDER = 'add_opr_order'


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


class TypeUpdate(str, Enum):
    ADD = 'add'
    ADD_OPR = 'add_opr'
    STATE = 'state'
    EDIT_COST = 'edit_cost'
    EDIT_COST_DELIVERY = 'edit_cost_dlv'
    NOT_COME = 'not_come'
    UP_DATE = 'up_date'

