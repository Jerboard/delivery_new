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
        # work_chats = {
        #     CompanyDLV.MASTER.value: -1001669708234,
        #     CompanyDLV.PUTILIN.value: -1001669708234,
        #     CompanyDLV.MASTER_SPB.value: -1001669708234,
        #     'group_expenses': -1001669708234,
        #     'group_report': -1001669708234,
        #     f'refuse_{CompanyDLV.MASTER.value}': -1001669708234,
        #     f'refuse_{CompanyDLV.PUTILIN.value}': -1001669708234,
        #     f'refuse_{CompanyDLV.MASTER_SPB.value}': -1001669708234,
        #     f'refuse_{CompanyDLV.POST.value}': -1001669708234,
        #     f'report_{CompanyDLV.MASTER.value}': -1001669708234,
        #     f'report_{CompanyDLV.PUTILIN.value}': -1001669708234,
        #     f'report_{CompanyDLV.MASTER_SPB.value}': -1001669708234,
        #     f'report_{CompanyDLV.POST.value}': -1001669708234,
        # }

    else:
        token = getenv ("TOKEN")
        db_url = getenv ('DB_URL')
        bot_name = 'MatrixDeliveryBot'
        host = getenv ('HOST')
        report_sheet_num = 8
        # work_chats = {
        #     CompanyDLV.MASTER.value: -1001838764189,
        #     CompanyDLV.PUTILIN.value: -1001864910335,
        #     CompanyDLV.MASTER_SPB.value: -1001653186290,
        #     'group_expenses': -1001903349475,
        #     'group_report': -1001863016934,
        #     f'refuse_{CompanyDLV.MASTER.value}': -1001997852647,
        #     f'refuse_{CompanyDLV.PUTILIN.value}': -1002141489538,
        #     f'refuse_{CompanyDLV.MASTER_SPB.value}': -1002097241384,
        #     f'refuse_{CompanyDLV.POST.value}': -1002117858384,
        #     f'report_{CompanyDLV.MASTER.value}': -1001863016934,
        #     f'report_{CompanyDLV.PUTILIN.value}': -1001887194825,
        #     f'report_{CompanyDLV.MASTER_SPB.value}': -1001971855032,
        #     f'report_{CompanyDLV.POST.value}': -1002062614241,
        # }

    tz = timezone('Europe/Moscow')
    day_form = '%d.%m'
    datetime_form = '%d.%m.%Y %H:%M'
    time_form = '%H:%M'

    file_google_path = os.path.join ('data', 'cred.json')
    data_path = 'data'
    # table_file = 'google_table.json'
    table_file = 'google_table.txt'
    opr_send_users_filename = 'opr_send_users_msg.json'
