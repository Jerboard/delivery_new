import re

import db
from utils.base_utils import get_order_cost
from data import base_data as dt
from enums import OrderStatus, UserRole, ShortText, KeyWords, CompanyDLV


# убирает пустые строки
def clearing_text(text: str) -> str:
    clear_text = ''
    for row in text.split ('\n'):
        if row and row[0] == '#':
            clear_text = f'{clear_text}\n{row[1:]}'
        elif not row or not re.search ('None', row):
            clear_text = f'{clear_text}\n{row}'

    return clear_text.replace('None', 'н/д').strip()


# текст заказа по строке
def get_order_text(order: db.OrderRow) -> str:
    cost = get_order_cost(order)
    bottom_text = '✖️ Клиент не явился' if order.d == KeyWords.NOT_COME.value else ''
    text = (
        f'Заказ от: {order.j} \n'
        f'Оператор: {order.k}\n'
        f'Клиент: {order.m}\n'
        f'Номер: <code>{order.n}</code> <code>{order.o}</code>\n'
        f'Доставка: {order.w}\n'
        f'Адрес: {order.x}\n'
        f'Цена: {cost} + {order.clmn_t}\n'
        f'Курьеру к оплате: {cost + order.clmn_t}\n'
        f'Примечания: {order.ab}\n\n'
        f'{bottom_text}'
    )
    return text.replace('None', '').strip()


# текст заказа для админов
def get_admin_order_text(order: db.OrderRow) -> str:
    prepay = order.u + order.v

    if order.q == 0 and prepay != 0:
        cost = 0
    else:
        # (q + r + s - y) + t
        cost = order.q + order.r + order.s - order.y

    status = dt.order_status_data.get(order.g)
    text = (f'#Заказ от {order.j}, исполнитель {order.h}\n'
            f'#Курьерская: {dt.company_dlv.get(order.ac)} ({order.f})\n'
            f'Номер курьера: {order.phone}\n'
            f'Статус заказа: {order.e} {status}\n\n'
            f'Оператор: {order.k}\n'
            f'ФИО: {order.m}\n'
            f'#Номер: <code>{order.n}</code> <code>{order.o}</code>\n'
            f'Метро: {order.w} \n'
            f'Адрес: {order.x}\n\n'
            f'Цена: {order.q}\n'
            f'Наценка: {order.r}\n'
            f'Доп: {order.s}\n'
            f'Доставка: {order.clmn_t}\n'
            f'Биток: {order.b}\n'
            f'Предоплата: {prepay}\n\n'
            f'Курьеру к оплате: {cost} + {order.clmn_t}\n'
            f'Итого: {cost + order.clmn_t}\n\n'
            f'Примечания: {order.ab}\n')

    return clearing_text(text)


# краткий заказ строка
def get_short_order_row(order: db.OrderRow, for_: str) -> str:
    cost = get_order_cost(order)

    if for_ in [UserRole.OWN.value, UserRole.OPR.value]:
        text = (f'<code>{order.n}</code>, <code>{order.o}</code>  {order.m} {order.x} '
                f'{order.f} {dt.order_status_data.get(order.g)}\n'.replace('None', ''))

    elif for_ == ShortText.ACTIVE.value:
        text = (f'{order.i} | {order.k} | {order.m} | <code>{order.n}</code> <code>{order.o}</code> '
                f'| {cost} + {order.clmn_t}| {order.w}')

    elif for_ == ShortText.FREE.value:
        # [ J ] | [ K ] | [ М ] | [ N ] [ O ] | ([ Q ]+[ R ]+[ S ]) + ([ T ]) | [ W ] | [ X ]
        text = (f'{order.j} | {order.k} | {order.m} | <code>{order.n}</code>  <code>{order.o}</code> |'
                f' {cost} + {order.clmn_t} | {order.w} | {order.x}')

    elif for_ == ShortText.REPORT.value:
        comment = f'({order.ab})' if order.ab else ''
        comment_d = f'({order.d})' if order.d else ''
        text = f'{comment_d} {dt.order_status_data.get (order.g)} {order.n} {cost} + {order.clmn_t} {order.w} {comment}\n'

    else:
        text = (f'<code>{order.n}</code>  <code>{order.o}</code> {cost} + {order.clmn_t} {order.w} '
                f'\n---------------------------\n')

    return text.replace('None', '')


def get_statistic_text(statistic: tuple[db.OrderGroupRow]) -> str:
    text = ''
    total = 0
    for order in statistic:
        # print(order)
        status = dt.order_status_data.get(order.status) if order.status != OrderStatus.NEW.value else 'Без курьера'
        if status:
            text += f'{status.capitalize()}: {order.orders_count}\n'
            total += order.orders_count
    return f'Всего заказов: {total}\n{text}'.strip()


# отчёт в группу при отказе от заказа
def get_dlv_refuse_text(order: db.OrderRow, note: str) -> str:
    cost = get_order_cost(order)
    return (
        f'Курьер: {order.f}\n'
        f'Номер курьера: {order.phone}\n\n'
        f'Оператор: {order.k}\n'
        f'Клиент: {order.m}\n'
        f'Номер: <code>{order.n}</code>, <code>{order.o}</code>\n'
        f'Доставка: {order.w}\n'
        f'Адрес: {order.x}\n'
        f'Цена: {cost} + {order.clmn_t}\n'
        f'Курьеру к оплате: {cost + order.clmn_t}\n'
        f'Примечания: {note}\n'
    ).replace('None', 'н/д')


# отчёты для операторов
def get_opr_report_text(order: db.OrderRow) -> str:
    cost = get_order_cost (order)
    return (
        f'🟠 {order.g} {order.e}\n'
        f'Курьер: {order.f} ({order.ac})\n\n'
        f'Оператор: {order.k}\n'
        f'ФИО: {order.m}\n'
        f'Номер: <code>{order.n}</code>, <code>{order.o}</code>\n'
        f'Цена: {cost}\n'
        f'Доставка: {order.clmn_t}\n'
        f'Метро: {order.w}\n'
        f'Адрес: {order.x}\n'
        f'Трек номер: {order.ac}\n'
    ).replace ('None', 'н/д')

