from enum import Enum


class BaseCB(str, Enum):
    TAKE_ORDER_1 = 'take_order_1'
    CLOSE = 'close'


class OwnerCB(str, Enum):
    BACK = 'own_back'
    UPDATE_TABLE = 'own_update_table'
    DEL_USER = 'own_del_user'
    SEND_MSG = 'own_send_msg'
    CHANGE_TAB = 'own_change_tab'
    VIEW_FREE_ORDERS = 'own_view_free_orders'
    UPDATE_USERS_TABLE = 'own_update_users_table'
    ADD_USER_1 = 'own_add_user_1'
    ADD_USER_2 = 'own_add_user_2'
    DEL_USER_1 = 'own_del_user_1'
    SEND_MSG_1 = 'own_send_msg_1'
    # CHANGE_TAB_1 = 'change_tab_1'
    VIEW_FREE_ORDERS_1 = 'own_view_free_orders_1'
    UPDATE_USERS_TABLE_1 = 'own_update_users_table_1'
    UPDATE_USERS_TABLE_2 = 'own_update_users_table_2'
    MAKE_ORDER_EMPTY = 'own_make_order_empty'
    TRANS_ORDER_1 = 'own_trans_order_1'
    TRANS_ORDER_2 = 'own_trans_order_2'


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
