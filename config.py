from dotenv import load_dotenv
from os import getenv
import os


load_dotenv ()
DEBUG = bool(int(getenv('DEBUG')))
# if DEBUG:


class config:
    token = getenv ("TOKEN")
    tz = 'Europe/Moscow'
    db_url = getenv ('DB_URL')
    bot_name = 'DeliveryChatStatusBot'
    group_expenses = -1001903349475
    group_report = -1001863016934
    day_form = '%d.%m'
    time_form = '%d.%m %H:%M'
    only_time_form = '%H:%M'
    file_google_path = os.path.join('data', 'cred.json')
    data_path = 'data'
    table_file = 'google_table'
    host = getenv('HOST')
    redis_port = getenv('REDIS_PORT')
    redis_db = 0
