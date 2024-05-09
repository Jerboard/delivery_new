import os
import json

import typing as t

from config import Config


# Сохраняет данные
def save_opr_msg_data(key: str, new_data: dict):
    filename = 'opr_send_users_msg.json'
    data_file_path = os.path.join(Config.data_path, filename)
    if not os.path.exists(data_file_path):
        data = {}
        with open (data_file_path, 'w') as file:
            json.dump (data, file)

    with open (data_file_path, 'r') as file:
        data: dict = json.load (file)

    data[key] = new_data
    with open (data_file_path, 'w') as file:
        json.dump (data, file)


# Извлекает данные
def get_opr_msg_data(key: str = None) -> t.Optional[dict]:
    filename = 'opr_send_users_msg.json'
    data_file_path = os.path.join (Config.data_path, filename)
    if os.path.exists (data_file_path):
        with open (data_file_path, 'r') as file:
            data: dict = json.load (file)

        if key:
            data = data.get(key)
        return data


# Удаляет данные
def del_opr_msg_data(key: str):
    filename = 'opr_send_users_msg.json'
    data_file_path = os.path.join (Config.data_path, filename)
    if os.path.exists (data_file_path):
        with open (data_file_path, 'r') as file:
            data: dict = json.load (file)

        del data[key]

        with open (data_file_path, 'w') as file:
            json.dump (data, file)
