import re

import db
from data import base_data as dt
from enums import OrderStatus, UserRole, ShortText


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
def get_order_text(order_info: db.OrderRow) -> str:
    prepay = order_info.u + order_info.v

    if order_info.q == 0 and prepay != 0:
        cost = 0
    else:
        cost = order_info.q + order_info.r + order_info.clmn_t - order_info.y

    text = f'Заказ от: {order_info.j} \n' \
           f'Оператор: {order_info.k}\n' \
           f'Клиент: {order_info.m}\n' \
           f'Номер: <code>{order_info.n}</code>    <code>{order_info.o}</code>      \n' \
           f'Доставка: {order_info.w}\n' \
           f'Адрес: {order_info.x}\n' \
           f'Цена: {cost} + {order_info.s}\n' \
           f'Курьеру к оплате: {cost + order_info.s}\n' \
           f'Примечания: {order_info.ab} '

    return text.replace('None', '').strip()


# текст заказа для админов
def get_admin_order_text(order: db.OrderRow) -> str:
    prepay = order.u + order.v

    if order.q == 0 and prepay != 0:
        cost = 0
    else:
        cost = order.q + order.r + order.clmn_t - order.y

    status = dt.order_status_data.get(order.g)
    text = (f'#Заказ от {order.j}, исполнитель {order.h}\n'
            f'#Курьерская: {dt.company.get(order.ac)} ({order.f})\n'
            f'Номер курьера: {order.phone} \n'
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
            f'Курьеру к оплате: ({ order.q + order.r + order.s}) + ({ order.clmn_t })\n'
            f'Итого: { order.q + order.r + order.s + order.clmn_t }\n\n'
            f'Примечания: {order.ab}\n')

    return clearing_text(text)


# краткий заказ строка
def get_short_order_row(order: db.OrderRow, for_: str) -> str:
    prepay = order.u + order.v
    cost = 0 if order.q == 0 and prepay != 0 else order.q + order.r + order.clmn_t - order.y
    cost_qrs = order.q + order.r + order.s

    if for_ in [UserRole.OWN.value, UserRole.OPR.value]:
        text = (f'<code>{order.n}</code>, <code>{order.o}</code>  {order.m} {order.x} '
                f'{order.f} {dt.order_status_data.get(order.g)}\n'.replace('None', ''))

    elif for_ == ShortText.ACTIVE.value:
        text = (f'{order.i} | {order.k} | {order.m} | <code>{order.n}</code> <code>{order.o}</code> '
                f'| {cost} + {order.s}| {order.w}')

    elif for_ == ShortText.FREE.value:
        text = (f'принят {order.j} | оператор {order.k} | ФИО {order.m} | '
                f'тел <code>{order.n}</code> тел2 <code>{order.o}</code> | '
                f'цена+наценка+доп {cost_qrs} + доставка {order.clmn_t} | метро {order.w} | адрес {order.x}')

    else:
        text = (f'<code>{order.n}</code>  <code>{order.o}</code> {cost} + {order.s} {order.w} '
                f'\n---------------------------\n')

    return text.replace('None', 'н/д')


def get_statistic_text(statistic: list[tuple]) -> str:
    text = ''
    total = 0
    for row in statistic:
        status = dt.order_status_data.get(row[0]) if row[0] != OrderStatus.NEW.value else 'Без курьера'
        if status:
            text += f'{status.capitalize()}: {row[1]}\n'
            total += row[1]
    return f'Всего заказов: {total}\n{text}'.strip()
