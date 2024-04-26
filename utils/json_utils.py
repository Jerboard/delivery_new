import json
import os

from config import config


# сохраняет json
def save_json_data(data: dict, file_name: str):
    path = os.path.join(config.data_path, f'{file_name}.json')
    with open(path, 'w') as file:
        json.dump(data, file)


# читает json
def get_json_data(file_name: str) -> dict:
    path = os.path.join (config.data_path, f'{file_name}.json')
    with open(path, 'r') as file:
        return json.load(file)

