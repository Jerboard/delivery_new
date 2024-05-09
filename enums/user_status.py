from enum import Enum


class DeliveryStatus(str, Enum):
    REG_NAME = 'reg_name'
    EDIT_NAME = 'edit_name'
    EDIT_ORDER_CLOSE_1 = 'edit_order_close_1'
    EDIT_ORDER_CLOSE_2 = 'edit_order_close_2'
    EXPENSES_3 = 'expenses_dvl_3'
    EXPENSES_4 = 'expenses_dvl_4'
    EXPENSES_5 = 'expenses_dvl_5'


class OwnerStatus(str, Enum):
    CHANGE_TAB = 'change_tab'
    VIEW_FREE_ORDERS = 'view_free_orders'


class OperatorStatus(str, Enum):
    TAKE_ORDER = 'take_order'
