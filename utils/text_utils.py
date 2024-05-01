import db

from data import base_data as dt
from enums import OrderStatus, UserRole


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
def get_short_order_row(order_info: db.OrderRow, for_: str) -> str:
    if for_ in [UserRole.OWN.value, UserRole.OPR.value]:
        return (f'<code>{order_info.n}</code>, <code>{order_info.o}</code>  {order_info.m} {order_info.x} '
            f'{order_info.f} {dt.order_status_data.get(order_info.g)}\n'.replace('None', ''))
    else:
        prepay = order_info.u + order_info.v

        if order_info.q == 0 and prepay != 0:
            cost = 0
        else:
            cost = order_info.q + order_info.r + order_info.clmn_t - order_info.y

        return (f'<code>{order_info.n}</code>  <code>{order_info.o}</code> {cost} + {order_info.s} {order_info.aa}'
                f'\n---------------------------\n')
