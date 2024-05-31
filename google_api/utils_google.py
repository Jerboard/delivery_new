import gspread
import logging
import asyncio

from gspread.spreadsheet import Spreadsheet
from datetime import datetime

import db
from config import Config
from init import TZ, bot
# import utils.json_utils as js
from utils.local_data_utils import get_table_id
from enums import OrderStatus


# (a - 0, b - 1, c - 2, d - 3, e - 4, f - 5, g - 6, h - 7, i - 8, j - 9, k - 10,
#  l - 11, m - 12, n - 13, o - 14, p - 15, q - 16, r - 17, s - 18, t - 19, u - 20,
#  v - 21, w - 22, x - 23, y - 24, z - 25.)
test_table = '12Sm-PMgBy_ANC2WuesE8WWo_sawyaqx4QeMlkWTVfmM'


def get_google_connect(table_id: str = None) -> Spreadsheet:
    gc = gspread.service_account (filename=Config.file_google_path)
    if not table_id:
        table_id = get_table_id()
    return gc.open_by_key (table_id)


# проверяет подключение к таблице
def is_table_exist(tab_id: str) -> bool:
    gc = gspread.service_account(filename=Config.file_google_path)
    try:
        gc.open_by_key(tab_id)
        return True
    except:
        return False


async def check_work_order_on_update(
        dlv_name_dict: dict,
        work_orders: list[int],
        order_id: int,
        order_status: str,
        order_user_name: str
) -> None:
    order_user_id = dlv_name_dict.get (order_user_name)

    if order_status == OrderStatus.NEW.value and order_id in work_orders:
        await db.delete_work_order (order_id=order_id)
    if not order_user_id:
        return
    if order_id in work_orders:
        await db.update_work_order (user_id=order_user_id, order_id=order_id)
    elif order_status in [OrderStatus.ACTIVE.value, OrderStatus.ACTIVE_TAKE.value]:
        await db.add_work_order (user_id=order_user_id, order_id=order_id)


async def add_order_in_google_table(sh: Spreadsheet, row_num: int, row: list, order_id: int):
    cell = f'a{row_num}:z{row_num}'
    row[0] = order_id
    sh.sheet1.update(cell, [row[:26]])
    await asyncio.sleep (1)
    cell = f'ab{row_num}'
    sh.sheet1.update (cell, row [27])
    logging.warning (f'Новая строка в таблицу:\n{row [:26]}\nAB: {row [27]}, Z: {row [25]} 24-30: {row [24:30]}')


async def update_order_in_google_table(sh: Spreadsheet, row: list):
    find_row = sh.sheet1.find (query=row[0], in_column=1)
    number_row = find_row.row
    cell = f'a{number_row}:z{number_row}'
    sh.sheet1.update(cell, [row[:26]])

    await asyncio.sleep(1)
    cell = f'ab{number_row}'
    sh.sheet1.update (cell, row [27])


# Очистить таблицу
def clear_new_order_table(sh: Spreadsheet, last_row: int):
    cell = f'a2:al{last_row + 1}'
    col = {"red": 1, "green": 1, "blue": 1}
    empty_list = [''] * 37
    del_list = [empty_list] * last_row
    sh.get_worksheet(1).update(cell, del_list)
    sh.get_worksheet(1).format (cell, {"backgroundColor": col})


#  подбирает цвет
def choice_color(status: str):
    print(status)
    if status in [OrderStatus.SUC.value, OrderStatus.SUC_TAKE.value]:
        color = {"red": 0.39, "green": 0.93, "blue": 0.54}
    elif status in [OrderStatus.ACTIVE.value, OrderStatus.ACTIVE_TAKE.value]:
        color = {"red": 1.0, "green": 1.0, "blue": 0.0}
    elif status in [OrderStatus.REF.value, OrderStatus.REF_TAKE.value]:
        color = {"red": 1.0, "green": 0.0, "blue": 0.0}
    else:
        color = {"red": 1.0, "green": 1.0, "blue": 1.0}
    return color
