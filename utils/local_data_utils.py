import os
import json

import typing as t

from config import Config
from utils.base_utils import get_today_date_str
from enums import Action, KeyWords


# создаёт необходимые файлы перед включением
def create_local_data_files():
    # заказы на забор
    data_file_path = os.path.join(Config.data_path, Config.opr_send_users_filename)
    if not os.path.exists(data_file_path):
        data = {}
        with open (data_file_path, 'w') as file:
            json.dump (data, file)

    # табличка гугл
    data_file_path = os.path.join (Config.data_path, Config.table_file_filename)
    if not os.path.exists (data_file_path):
        data = {}
        with open (data_file_path, 'w') as file:
            json.dump (data, file)

    # заказы почтовых курьеров
    data_file_path = os.path.join (Config.data_path, Config.active_post_orders_filename)
    if not os.path.exists (data_file_path):
        data = {}
        with open (data_file_path, 'w') as file:
            json.dump (data, file)


# Сохраняет данные
def save_opr_msg_data(key: str, new_data: dict):
    data_file_path = os.path.join(Config.data_path, Config.opr_send_users_filename)

    with open (data_file_path, 'r') as file:
        data: dict = json.load (file)

    data[key] = new_data
    with open (data_file_path, 'w') as file:
        json.dump (data, file)


# Извлекает данные
def get_opr_msg_data(key: str = None) -> t.Optional[dict]:
    data_file_path = os.path.join(Config.data_path, Config.opr_send_users_filename)
    if os.path.exists (data_file_path):
        with open (data_file_path, 'r') as file:
            data: dict = json.load (file)

        if key:
            data = data.get(key)
        return data


# Удаляет данные
def del_opr_msg_data(key: str):
    data_file_path = os.path.join (Config.data_path, Config.opr_send_users_filename)
    if os.path.exists (data_file_path):
        with open (data_file_path, 'r') as file:
            data: dict = json.load (file)

        del data[key]

        with open (data_file_path, 'w') as file:
            json.dump (data, file)


# сохраняет id таблицы
def save_table_id(table_id: str):
    path = os.path.join (Config.data_path, Config.table_file_filename)
    with open(path, 'w', encoding='utf-8') as file:
        file.write(table_id)


# возвращает id таблицы
def get_table_id() -> str:
    path = os.path.join (Config.data_path, Config.table_file_filename)
    with open (path, 'r', encoding='utf-8') as file:
        return file.read ().strip ()


# Сохраняет данные заказов почтовиков
def edit_post_order_ld(user_id: int, action: str, key_1: str, order_id: int = None):
    key = str (user_id)
    data_file_path = os.path.join(Config.data_path, Config.active_post_orders_filename)

    with open (data_file_path, 'r') as file:
        data: dict = json.load (file)

    user_data: dict = data.get(key, {})
    if action == Action.ADD:
        if key_1 == KeyWords.ID:
            ids_list: list = data.get(key_1, [])
            ids_list.append(order_id)
            data [key] [key_1] = list (set (user_data))

        else:
            data[key][key_1] = get_today_date_str()

    elif action == Action.DEL.value:
        if key_1 == KeyWords.ID:
            ids_list: list = data.get (key_1, [])
            ids_list.remove (order_id)
            data [key] [key_1] = list (set (user_data))
        else:
            data[key][key_1] = None

    with open (data_file_path, 'w') as file:
        json.dump (data, file)


# Извлекает данные заказов почтовиков
def get_post_order_ld(user_id: int) -> dict:
    key = str(user_id)
    data_file_path = os.path.join(Config.data_path, Config.active_post_orders_filename)
    with open (data_file_path, 'r') as file:
        data: dict = json.load (file)

    return data.get(key, {})
