from enum import Enum


class BaseCB(str, Enum):
    TAKE_ORDER_1 = 'take_order_1'
    CLOSE = 'close'


class OwnerCB(str, Enum):
    UPDATE_TABLE = 'update_table'
    ADD_USER_DLV = 'add_user_dlv'
    DEL_USER = 'del_user'
    SEND_MSG = 'send_msg'
    CHANGE_TAB = 'change_tab'
    VIEW_FREE_ORDERS = 'view_free_orders'
    UPDATE_USERS_TABLE = 'update_users_table'
    ADD_USER_1 = 'add_user_1'
    DEL_USER_1 = 'del_user_1'
    SEND_MSG_1 = 'send_msg_1'
    # CHANGE_TAB_1 = 'change_tab_1'
    VIEW_FREE_ORDERS_1 = 'view_free_orders_1'
    UPDATE_USERS_TABLE_1 = 'update_users_table_1'
    UPDATE_USERS_TABLE_2 = 'update_users_table_2'


class DeliveryCB(str, Enum):
    DLV_ORDER_1 = 'dlv_order_1'
    DLV_ORDER_2 = 'dlv_order_2'
    DLV_ORDER_3 = 'dlv_order_3'
    DLV_ORDER_4 = 'dlv_order_4'
    DLV_ORDER_5 = 'dlv_order_5'
    DLV_ORDER_6 = 'dlv_order_6'
    TAKE_ORDER_2 = 'take_order_2'
    EDIT_DLV_NAME = 'edit_dlv_name'
    REPORT_DVL_1 = 'report_dvl_1'
    REPORT_DVL_2 = 'report_dvl_2'
    REPORT_DVL_3 = 'report_dvl_3'
    REPORT_DVL_4 = 'report_dvl_4'
    EXPENSES_DVL_1 = 'expenses_dvl_1'
    EXPENSES_DVL_2 = 'expenses_dvl_2'
    EXPENSES_DVL_3 = 'expenses_dvl_3'
    EXPENSES_DVL_4 = 'expenses_dvl_4'
    EXPENSES_DVL_5 = 'expenses_dvl_5'
    EXPENSES_DVL_VIEW = 'expenses_dvl_view'
    BACK_MAIN_ORDER = 'back_main_order'
    TRANS_ORDER = 'dlv_trans_order'
    BACK_DLV_MAIN = 'back_dlv_main'
