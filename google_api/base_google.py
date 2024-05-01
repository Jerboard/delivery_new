import gspread
import asyncio

from gspread.spreadsheet import Spreadsheet
from datetime import datetime

import db
import utils.json_utils as js
import google_api.utils_google as ug
from config import config
from init import TZ, bot, log_error
from data.base_data import order_status_data
from enums import TypeUpdate


# (a - 0, b - 1, c - 2, d - 3, e - 4, f - 5, g - 6, h - 7, i - 8, j - 9, k - 10,
#  l - 11, m - 12, n - 13, o - 14, p - 15, q - 16, r - 17, s - 18, t - 19, u - 20,
#  v - 21, w - 22, x - 23, y - 24, z - 25.)
test_table = '12Sm-PMgBy_ANC2WuesE8WWo_sawyaqx4QeMlkWTVfmM'


# обновляет таблицу по команде
async def save_new_order_table() -> None:
    sh = ug.get_google_connect ()

    new_orders = sh.sheet1.get_all_values ()

    new_row = 4
    # 4985 - 4978
    for row in new_orders [4:]:
        new_row += 1
        if row [13].strip () != '' and row[0].isdigit():
            # print(f'row: {new_row} - {row[0]} :id')
            try:
                await db.add_row (
                    empty_id=int(row[0]),
                    row_num=new_row,
                    b=row [1].strip () if row [1] else None,
                    c=row [2].strip () if row [2] else None,
                    d=row [3].strip () if row [3] else None,
                    e=row [4].strip () if row [4] else None,
                    f=row [5].strip () if row [5] else None,
                    g=order_status_data.get(row[6].strip()),
                    h=row [7].strip () if row [7] else None,
                    i=row [8].strip () if row [8] else None,
                    j=row [9].strip () if row [9] else None,
                    k=row [10].strip () if row [10] else None,
                    l=row [11].strip () if row [11] else None,
                    m=row [12].strip () if row [12] else None,
                    n=row [13].strip () if row [13] else None,
                    o=row [14].strip () if row [14] else '',
                    p=row [15].strip () if row [15] else None,
                    q=int (row [16]) if row [16] else 0,
                    r=int (row [17]) if row [17] else 0,
                    s=int (row [18]) if row [18] else 0,
                    t=int (row [19]) if row [19] else 0,
                    u=int (row [20]) if row [20] else 0,
                    v=int (row [21]) if row [21] else 0,
                    w=row [22].strip () if row [22] else None,
                    x=row [23].strip () if row [23] else None,
                    y=int (row [24]) if row [24] else 0,
                    z=row [25].strip () if row [25] else None,
                    aa=row [26].strip () if row [26] else None,
                    ab=row [27].strip () if row [27] else None,
                    ac=row [28].strip () if row [28] else None,
                    ad=row [29].strip () if row [29] else None,
                    ae=row [30].strip () if row [30] else None,
                    af=row [31].strip () if row [31] else None,
                    ag=row [32].strip () if row [32] else None,
                    ah=row [33].strip () if row [33] else None,
                    type_update=TypeUpdate.ADD.value,
                    updated=True
                )
            except Exception as ex:
                log_error (ex, with_traceback=False)


# сохраняет таблицу отчётов
async def save_new_report_table() -> None:
    sh = ug.get_google_connect ()
    table = sh.get_worksheet (6).get_all_values ()
    counter = 4
    for row in table [5:]:
        counter += 1
        try:
            if row [0].isdigit ():
                l_list = row [11].split ('\n')
                await db.add_report_row (
                    entry_id=int (row [0]),
                    b=int (row [1]) if row [1] else 0,
                    c=int (row [2]) if row [2] else 0,
                    d=int (row [3]) if row [3] else 0,
                    e=int (row [4]) if row [4] else 0,
                    f=int (row [5]) if row [5] else 0,
                    g=int (row [6]) if row [6] else 0,
                    h=int (row [7]) if row [7] else 0,
                    i=int (row [8]) if row [8] else 0,
                    k=int (row [9]) if row [9] else 0,
                    l=l_list,
                    m=row [12].strip (),
                    n=row [13].strip (),
                    o=int (row [14]) if row [14] else 0,
                    p=row [15].strip (),
                    q=row [16].strip (),
                    r=int (row [17]) if row [17] else 0,
                    updated=True,
                    row_num=counter
                )
        except Exception as ex:
            log_error(ex)


# обновляет таблицу по команде
async def update_google_table(user_id: int) -> None:
    time_start = datetime.now()
    sh = ug.get_google_connect()

    # основные параметры
    new_orders = sh.sheet1.get_all_values()
    last_row = await db.get_max_row_num()
    if not last_row:
        last_row = 4
    new_row = last_row + 1

    # ug.clear_new_order_table(sh, len(new_orders))
    exception_list = []

    i = 0
    for row in new_orders[4:100]:
        if row[13].strip() != '':
            i += 1
            if row[0].isdigit():
                try:
                    await db.update_row_google(
                        order_id=int(row[0]),
                        update_row=True,
                        all_row=True,
                        b=row[1].strip() if row[1] else None,
                        c=row[2].strip() if row[2] else None,
                        d=row[3].strip() if row[3] else None,
                        e=row[4].strip() if row[4] else None,
                        f=row[5].strip() if row[5] else None,
                        g=order_status_data.get (row [6].strip ()),
                        h=row[7].strip() if row[7] else None,
                        i=row[8].strip() if row[8] else None,
                        j=row[9].strip() if row[9] else None,
                        k=row[10].strip() if row[10] else None,
                        l=row[11].strip() if row[11] else None,
                        m=row[12].strip() if row[12] else None,
                        n=row[13].strip() if row[13] else None,
                        o=row[14].strip() if row[14] else '',
                        p=row[15].strip() if row[15] else None,
                        q=int(row[16]) if row[16] else 0,
                        r=int(row[17]) if row[17] else 0,
                        s=int(row[18]) if row[18] else 0,
                        t=int(row[19]) if row[19] else 0,
                        u=int(row[20]) if row[20] else 0,
                        v=int(row[21]) if row[21] else 0,
                        w=row[22].strip() if row[22] else None,
                        x=row[23].strip() if row[23] else None,
                        y=int(row[24]) if row[24] else 0,
                        z=row[25].strip() if row[25] else None,
                        aa=row[26].strip() if row[26] else None,
                        ab=row[27].strip() if row[27] else None,
                        ac=row[28].strip() if row[28] else None,
                        ad=row[29].strip() if row[29] else None,
                        ae=row[30].strip() if row[30] else None,
                        af=row[31].strip() if row[31] else None,
                        ag=row[32].strip() if row[32] else None,
                        ah=row[33].strip() if row[33] else None,
                    )
                except Exception as ex:
                    exception_list.append(row[:24])
                    log_error (ex)
                    text = f'Не удалось обновить заказ ID {row[0]}'
                    await bot.send_message(user_id, text, disable_notification=True)

            else:
                try:
                    await db.add_row(
                        row_num=new_row,
                        b=row[1].strip() if row[1] else None,
                        c=row[2].strip() if row[2] else None,
                        d=row[3].strip() if row[3] else None,
                        e=row[4].strip() if row[4] else None,
                        f=row[5].strip() if row[5] else None,
                        g=order_status_data.get (row [6].strip ()),
                        h=row[7].strip() if row[7] else None,
                        i=row[8].strip() if row[8] else None,
                        j=row[9].strip() if row[9] else None,
                        k=row[10].strip() if row[10] else None,
                        l=row[11].strip() if row[11] else None,
                        m=row[12].strip() if row[12] else None,
                        n=row[13].strip() if row[13] else None,
                        o=row[14].strip() if row[14] else '',
                        p=row[15].strip() if row[15] else None,
                        q=int(row[16]) if row[16] else 0,
                        r=int(row[17]) if row[17] else 0,
                        s=int(row[18]) if row[18] else 0,
                        t=int(row[19]) if row[19] else 0,
                        u=int(row[20]) if row[20] else 0,
                        v=int(row[21]) if row[21] else 0,
                        w=row[22].strip() if row[22] else None,
                        x=row[23].strip() if row[23] else None,
                        y=int(row[24]) if row[24] else 0,
                        z=row[25].strip() if row[25] else None,
                        aa=row[26].strip() if row[26] else None,
                        ab=row[27].strip() if row[27] else None,
                        ac=row[28].strip() if row[28] else None,
                        ad=row[29].strip() if row[29] else None,
                        ae=row[30].strip() if row[30] else None,
                        af=row[31].strip() if row[31] else None,
                        ag=row[32].strip() if row[32] else None,
                        ah=row[33].strip() if row[33] else None,
                        type_update=TypeUpdate.ADD.value,
                        updated=True
                    )
                    new_row += 1
                except Exception as ex:
                    exception_list.append (row)
                    log_error(ex)
                    text = f'Не удалось добавить заказ {row.n} {row.m}'
                    await bot.send_message (user_id, text, disable_notification=True)

    if exception_list:
        try:
            cell = f'a2:ah{len(exception_list) + 1}'
            sh.get_worksheet(1).update(cell, exception_list)
        except Exception as ex:
            log_error(message=f'Ошибка при возвращении ошибок таблицы: {ex}\n\n'
                              f'{exception_list}', with_traceback=False)
    print (datetime.now () - time_start)


# добавляет одно последнее изменение в таблицу
async def update_google_row() -> None:
    order = await db.get_order(for_update=True)

    if order:
        sh = ug.get_google_connect()
        # изменяет статус заказа
        try:
            cell = f'A{order.row_num}:Z{order.row_num}'
            new_row_str = [
                [
                    str(order.id) if order.id else '', str(order.b) if order.b else '',
                    str(order.c) if order.c else '', str(order.d) if order.d else '',
                    str(order.e) if order.e else '', str(order.f) if order.f else '',
                    order_status_data.get (order.g), str(order.h) if order.h else '',
                    str(order.i) if order.i else '', str(order.j) if order.j else '',
                    str(order.k) if order.k else '', str(order.l) if order.l else '',
                    str(order.m) if order.m else '', str(order.n) if order.n else '',
                    str(order.o) if order.o else '', str(order.p) if order.p else '',
                    str(order.q) if order.q else '', str(order.r) if order.r else '',
                    str(order.s) if order.s else '', str(order.clmn_t) if order.clmn_t else '',
                    str(order.u) if order.u else '', str(order.v) if order.v else '',
                    str(order.w) if order.w else '', str(order.x) if order.x else '',
                    str(order.y) if order.y else '', str(order.z) if order.z else ''
                ]
            ]
            sh.sheet1.update (cell, new_row_str)

            if order.type_update == TypeUpdate.STATE.value:
                color = ug.choice_color(order.g)
                cell_form = f'E{order.row_num}:G{order.row_num}'
                sh.sheet1.format(cell_form, {"backgroundColor": color})

            # изменяет стоимость заказа
            elif order.type_update == TypeUpdate.EDIT_COST.value:
                color = {"red": 1.0, "green": 0.0, "blue": 0.0}
                sh.sheet1.update(f'AB{order.row_num}', order.ab)
                sh.sheet1.format(f'AB{order.row_num}', {"backgroundColor": color})

            # изменяет стоимость доставки
            elif order.type_update == TypeUpdate.EDIT_COST_DELIVERY.value:
                color = {"red": 2.0, "green": 0.0, "blue": 0.0}
                sh.sheet1.update(f'AB{order.row_num}', order.ab)
                sh.sheet1.format(f'T{order.row_num}', {"backgroundColor": color})
                sh.sheet1.format(f'AB{order.row_num}', {"backgroundColor": color})
                
            elif order.type_update == TypeUpdate.ADD_OPR.value:
                col = {"red": 0.0, "green": 1.0, "blue": 1.0}
                sh.sheet1.update (f'AB{order.row_num}', order.ab)
                cell = f'A{order.row_num}:AC{order.row_num}'
                sh.sheet1.format (cell, {"backgroundColor": col})

                # помечает не явился
            # elif order['type'] == 'not_come':
            #     sh.sheet1.update(f'AB{order.row_num}', order['ab'])

                # обновляет дату
            # elif order['type'] == 'up_date':
            #     sh.sheet1.update(f'E{order.row_num}', order['e'])

                # даёт ид
            # elif order[35] == 'get_id':
            #     sh.sheet1.update(f'A{order.row_num}', order[1])

            # else:
            #     log_error(f'Ошибка записи из таблицы темп:\n{order}', with_traceback=False)

            await db.update_row_google(order_id=order.id, update_row=True)

        except Exception as ex:
            log_error(f'Заказ не добавлен из таблицы темп ошибка:\n{order}', with_traceback=False)
            log_error(ex)


# записывает данные в отчёт курьера
async def insert_google_expenses():
    new_row = await db.get_last_updated_report()
    if new_row:
        sh = ug.get_google_connect()
        try:
            cell = f"A{new_row.row_num}:R{new_row.row_num}"
            l_str = '\n'.join(new_row.l)
            new_row_str = [
                [
                    str(new_row.id) if new_row.b else '', str(new_row.b) if new_row.b else '',
                    str(new_row.c) if new_row.c else '', str(new_row.d) if new_row.d else '',
                    str(new_row.e) if new_row.e else '', str(new_row.f) if new_row.f else '',
                    str(new_row.g) if new_row.g else '', str(new_row.h) if new_row.h else '',
                    str(new_row.i) if new_row.i else '', str(new_row.j) if new_row.j else '',
                    str(new_row.k) if new_row.k else '', l_str,
                    str(new_row.m) if new_row.m else '', str(new_row.n) if new_row.n else '',
                    str(new_row.o) if new_row.o else '', str(new_row.p) if new_row.p else '',
                    str(new_row.q) if new_row.q else '', str(new_row.r) if new_row.r else ''
                ]
            ]

            sh.get_worksheet(6).update(cell, new_row_str)
            await db.update_expenses_dlv(entry_id=new_row.id, updated=True)
        except Exception as ex:
            log_error(f'Не получилось обновить отчёт {new_row.m} {new_row.n}', with_traceback=False)
            log_error(ex)


async def update_report_table():
    sh = ug.get_google_connect()
    table = sh.get_worksheet(6).get_all_values()
    counter = 4
    for row in table[5:]:
        print(row)
        counter += 1
        if row[0].isdigit():
            l_list = row[11].split('\n')
            await db.add_report_row(
                entry_id=int(row[0]) if row[0] else counter,
                b=int(row[1]) if row[1] else 0,
                c=int(row[2]) if row[2] else 0,
                d=int(row[3]) if row[3] else 0,
                e=int(row[4]) if row[4] else 0,
                f=int(row[5]) if row[5] else 0,
                g=int(row[6]) if row[6] else 0,
                h=int(row[7]) if row[7] else 0,
                i=int(row[8]) if row[8] else 0,
                k=int(row[9]) if row[9] else 0,
                l=l_list,
                m=row[12].strip(),
                n=row[13].strip(),
                o=int(row[14]) if row[14] else 0,
                p=row[15].strip(),
                q=row[16].strip(),
                r=int(row[17]) if row[17] else 0,
                updated=True,
                row_num=counter
            )


# добавляет курьеров и компании в таблицу
def add_users_table():
    pass
    # dlv_table = db.get_dlv_table()
    # comp_table = db.get_comp_table()

    # sh = ug.get_google_connect()
    # table = []
    # for line in dlv_table:
    #     row = []
    #     for cell in line:
    #         row.append(cell)
    #     table.append(row)
    #
    # sh.get_worksheet(7).update(f'a3:d{len(table) + 3}', table)
    #
    # table = []
    # for line in comp_table:
    #     row = []
    #     for cell in line:
    #         row.append(cell)
    #     table.append(row)
    #
    # sh.get_worksheet(7).update(f'f3:g{len(table) + 3}', table)


# обновляет данные по курьерам
def update_users_table():
    sh = ug.get_google_connect()
    all_table = sh.get_worksheet(7).get_all_values()

    # result = db.get_all_users_id()
    # list_exception = [user_id[0] for user_id in result]
    #
    # for row in all_table[2:]:
    #     if row[0] in list_exception:
    #         db.update_user_data(row)
    #
    #     elif row[0] is not None or row[0] != '':
    #         db.add_user_data(row)
    #
    # result = db.get_all_comp_id()
    # list_exception = [comp_id[0] for comp_id in result]
    #
    # for row in all_table[2:]:
    #     try:
    #         if int(row[5]) in list_exception:
    #             db.update_comp_dlv(row)
    #
    #     except Exception as ex:
    #         logging.warning(f'update_users_table 495:\n{ex}')
