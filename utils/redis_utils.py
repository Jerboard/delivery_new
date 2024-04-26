from init import redis_client

import json
import typing as t
from datetime import timedelta


# добавляет данные в редис с временем жизни
def add_data_in_redis(key: str, data: t.Union[dict, list]) -> None:
    live_time = timedelta(days=2)
    save_data = json.dumps(data)
    redis_client.setex (name=key, time=live_time, value=save_data)
    # redis_client.set (key, save_data)


# извлекает данные из редиса
def get_redis_data(key: str) -> t.Union[dict, list]:
    data = redis_client.get (key)
    if data:
        return json.loads (data.decode ("utf-8"))
