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
        bot_name = 'MatrixDeliveryBot'
        host = getenv('HOST')
        report_sheet_num = 6
        work_chats = {
            CompanyDLV.MASTER.value: -1001669708234,
            CompanyDLV.PUTILIN.value: -1001669708234,
            CompanyDLV.MASTER_SPB.value: -1001669708234,
            'group_expenses': -1001669708234,
            'group_report': -1001669708234
        }

    else:
        token = getenv ("TOKEN")
        db_url = getenv ('DB_URL')
        bot_name = 'MatrixDeliveryBot'
        host = getenv ('HOST')
        report_sheet_num = 8
        work_chats = {
            CompanyDLV.MASTER.value: -1001838764189,
            CompanyDLV.PUTILIN.value: -1001864910335,
            CompanyDLV.MASTER_SPB.value: -1001653186290,
            'group_expenses': -1001903349475,
            'group_report': -1001863016934
        }

    tz = timezone('Europe/Moscow')
    day_form = '%d.%m'
    datetime_form = '%d.%m.%Y %H:%M'
    time_form = '%H:%M'

    file_google_path = os.path.join ('data', 'cred.json')
    data_path = 'data'
    # table_file = 'google_table.json'
    table_file = 'google_table.txt'
    opr_send_users_filename = 'opr_send_users_msg.json'
