import db

from data import base_data as dt
from enums import OrderStatus, UserRole, ShortText


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
def get_admin_order_text(order_info: db.OrderRow) -> str:
    prepay = order_info.u + order_info.v

    if order_info.q == 0 and prepay != 0:
        cost = 0
    else:
        cost = order_info.q + order_info.r + order_info.clmn_t - order_info.y

    text = (f'Когда выдан: {order_info.i}\n'
            f'Исполнитель: {order_info.f}\n\n'
            f'Оператор: {order_info.k}\n'
            f'ФИО: {order_info.m}\n'
            f'Номер: <code>{order_info.n}</code>  <code>{order_info.o}</code>\n'
            f'Доставка: {order_info.clmn_t}\n'
            f'Адрес: {order_info.x}\n\n'
            f'Цена: {order_info.q} \n'
            f'Наценка: {order_info.r}\n'
            f'Доп: {order_info.s}\n'
            f'Доставка: {order_info.clmn_t}\n\n'
            f'СБЕР | Тинькофф: {order_info.u + order_info.v}\n'
            f'Курьеру к оплате: {cost} + {order_info.s}\n'
            f'Курьерская: {order_info.ac} ({order_info.f})\n'
            f'Статус заказа: {dt.order_status_data.get(order_info.g)}\n'
            f'Примечания: {order_info.ab}')

    return text.replace('None', '').strip()


# краткий заказ строка
def get_short_order_row(order: db.OrderRow, for_: str) -> str:
    prepay = order.u + order.v
    cost = 0 if order.q == 0 and prepay != 0 else order.q + order.r + order.clmn_t - order.y

    if for_ in [UserRole.OWN.value, UserRole.OPR.value]:
        text = (f'<code>{order.n}</code>, <code>{order.o}</code>  {order.m} {order.x} '
                f'{order.f} {dt.order_status_data.get(order.g)}\n'.replace('None', ''))

    elif for_ == ShortText.ACTIVE.value:
        text = (f'{order.i} | {order.k} | {order.m} | <code>{order.n}</code> <code>{order.o}</code> '
                f'| {cost} + {order.s}| {order.w}')

    elif for_ == ShortText.FREE.value:
        text = f'{order.e} | {order.g} | {order.l} | <code>{order.n}</code> <code>{order.o}</code> ' \
                     f'| {cost} + {order.s}| {order.w}'

    else:
        text = (f'<code>{order.n}</code>  <code>{order.o}</code> {cost} + {order.s} {order.w} '
                f'\n---------------------------\n')

    return text.replace('None', 'н/д').strip()


def get_statistic_text(statistic: list[tuple]) -> str:
    text = ''
    total = 0
    for row in statistic:
        status = dt.order_status_data.get(row[0]) if row[0] != OrderStatus.NEW.value else 'Без курьера'
        if status:
            text += f'{status.capitalize()}: {row[1]}\n'
            total += row[1]
    return f'Всего заказов: {total}\n{text}'.strip()
