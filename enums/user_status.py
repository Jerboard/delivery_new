from enum import Enum


class DeliveryStatus(str, Enum):
    REG_NAME = 'reg_name'
    EDIT_NAME = 'edit_name'
    EDIT_ORDER_CLOSE_1 = 'edit_order_close_1'
    EDIT_ORDER_CLOSE_2 = 'edit_order_close_2'
    EXPENSES_DVL_3 = 'expenses_dvl_3'
    EXPENSES_DVL_4 = 'expenses_dvl_4'
    EXPENSES_DVL_5 = 'expenses_dvl_5'


class OwnerStatus(str, Enum):
    CHANGE_TAB = 'change_tab'
