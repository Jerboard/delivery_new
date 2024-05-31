from enum import Enum


class BaseCB(str, Enum):
    TAKE_ORDER_1 = 'take_order_1'
    CLOSE = 'close'


class OwnerCB(str, Enum):
    BACK = 'own_back'
    UPDATE_TABLE = 'own_update_table'
    CHANGE_TAB = 'own_change_tab'
    VIEW_FREE_ORDERS = 'own_view_free_orders'
    UPDATE_USERS_TABLE = 'own_update_users_table'
    ADD_USER_1 = 'own_add_user_1'
    ADD_USER_2 = 'own_add_user_2'
    DEL_USER_1 = 'own_del_user_1'
    DEL_USER_2 = 'own_del_user_2'
    VIEW_ORDERS_1 = 'own_view_orders_1'
    VIEW_ORDERS_2 = 'own_view_orders_2'
    VIEW_FREE_ORDERS_1 = 'own_view_free_orders_1'
    UPDATE_USERS_TABLE_1 = 'own_update_users_table_1'
    UPDATE_USERS_TABLE_2 = 'own_update_users_table_2'
    MAKE_ORDER_FREE = 'own_make_order_free'
    ADD_ORDER = 'own_add_order'
    TRANS_ORDER_1 = 'own_trans_order_1'
    TRANS_ORDER_2 = 'own_trans_order_2'
    BACK_FREE = 'own_free_back_order'


class DeliveryCB(str, Enum):
    ORDER_1 = 'dlv_order_1'
    ORDER_2 = 'dlv_order_2'
    ORDER_3 = 'dlv_order_3'
    ORDER_4 = 'dlv_order_4'
    ORDER_5 = 'dlv_order_5'
    ORDER_6 = 'dlv_order_6'
    ORDER_7 = 'dlv_order_7'
    TAKE_ORDER_2 = 'dlv_take_order_2'
    EDIT_NAME = 'dlv_edit_name'
    REPORT_1 = 'dlv_report_1'
    REPORT_2 = 'dlv_report_2'
    REPORT_3 = 'dlv_report_3'
    REPORT_4 = 'dlv_report_4'
    EXPENSES_1 = 'dlv_expenses_1'
    EXPENSES_2 = 'dlv_expenses_2'
    EXPENSES_3 = 'dlv_expenses_3'
    EXPENSES_4 = 'dlv_expenses_4'
    EXPENSES_5 = 'dlv_expenses_5'
    EXPENSES_VIEW = 'dlv_expenses_view'
    BACK_MAIN = 'dlv_back_main_menu'
    BACK_MAIN_ORDER = 'dlv_back_main_order'
    BACK_CLOSE_ORDER = 'dlv_back_close_order'
    TRANS_ORDER = 'dlv_trans_order'


class OperatorCB(str, Enum):
    TAKE_ORDER_1 = 'opr_take_order_1'
    TAKE_ORDER_2 = 'opr_take_order_2'
