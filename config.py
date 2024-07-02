from dotenv import load_dotenv
from os import getenv
from pytz import timezone
import os

from enums import CompanyDLV


load_dotenv ()
DEBUG = bool(int(getenv('DEBUG')))


class Config:
    if DEBUG:
        token = getenv ("TOKEN_TEST")
        db_url = getenv ('DB_URL')
        # db_url = getenv ('DB_URL_WORK')
        bot_name = 'tushchkan_test_3_bot'
        host = getenv('HOST')

    else:
        token = getenv ("TOKEN")
        db_url = getenv ('DB_URL')
        bot_name = 'MatrixDeliveryBot'
        host = getenv ('HOST')

    report_sheet_num = 6
    tz = timezone('Europe/Moscow')
    day_form = '%d.%m'
    datetime_form = '%d.%m.%Y %H:%M'
    time_form = '%H:%M'

    file_google_path = os.path.join ('data', 'cred.json')
    data_path = 'data'
    # table_file = 'google_table.json'
    table_file_filename = 'google_table.txt'
    opr_send_users_filename = 'opr_send_users_msg.json'
    expenses_log = 'expenses_log.txt'
