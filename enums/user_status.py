from enum import Enum


class DeliveryStatus(str, Enum):
    REG_NAME = 'reg_name'
    REG_PHONE = 'reg_phone'
    EDIT_NAME = 'edit_name'
    EDIT_ORDER_CLOSE_1 = 'edit_order_close_1'
    EDIT_ORDER_CLOSE_2 = 'edit_order_close_2'
    EXPENSES_3 = 'expenses_dvl_3'
    EXPENSES_4 = 'expenses_dvl_4'


class OwnerStatus(str, Enum):
    CHANGE_TAB = 'change_tab'
    VIEW_FREE_ORDERS = 'view_free_orders'
    ADD_ORDER = 'own_add_order'


class OperatorStatus(str, Enum):
    TAKE_ORDER = 'take_order'
