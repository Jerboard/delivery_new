import os
import json

import typing as t

from config import Config


# создаёт необходимые файлы перед включением
def create_local_data_files():
    data_file_path = os.path.join(Config.data_path, Config.opr_send_users_filename)
    if not os.path.exists(data_file_path):
        data = {}
        with open (data_file_path, 'w') as file:
            json.dump (data, file)

    data_file_path = os.path.join (Config.data_path, Config.table_file)
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
