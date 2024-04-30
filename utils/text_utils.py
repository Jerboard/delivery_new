import db

from enums import OrderStatus


# текст заказа по строке
def get_order_text(order_info: db.OrderRow) -> str:
    prepay = order_info.u + order_info.v

    if order_info.q == 0 and prepay != 0:
        cost = 0
    else:
        cost = order_info.q + order_info.r + order_info.t - order_info.y

    text = f'Заказ от: {order_info.j} \n' \
           f'Оператор: {order_info.k}\n' \
           f'Клиент: {order_info.m}\n' \
           f'Номер: <code>{order_info.n}</code>    <code>{order_info.o}</code>      \n' \
           f'Доставка: {order_info.w}\n' \
           f'Адрес: {order_info.x}\n' \
           f'Цена: {cost} + {order_info.s}\n' \
           f'Курьеру к оплате: {cost + order_info.s}\n' \
           f'Примечания: {order_info.ab} '

    return text.strip()


# текст заказа для админов
def get_admin_order_text(order_info: db.OrderRow) -> str:
    prepay = order_info.u + order_info.v

    if order_info.q == 0 and prepay != 0:
        cost = 0
    else:
        cost = order_info.q + order_info.r + order_info.t - order_info.y

    text = (f'Когда выдан: {order_info.i}\n'
            f'Исполнитель: {order_info.f}\n\n'
            f'Оператор: {order_info.k}\n'
            f'ФИО: {order_info.m}\n'
            f'Номер: <code>{order_info.n}</code>  <code>{order_info.o}</code>\n'
            f'Доставка: {order_info.t}\n'
            f'Адрес: {order_info.x}\n\n'
            f'Цена: {order_info.q} \n'
            f'Наценка: {order_info.r}\n'
            f'Доп: {order_info.s}\n'
            f'Доставка: {order_info.t}\n\n'
            f'СБЕР | Тинькофф: {order_info.u + order_info.v}\n'
            f'Курьеру к оплате: {cost} + {order_info.s}\n'
            f'Курьерская: {order_info.ac} ({order_info.f})\n'
            f'Статус заказа: {order_info.g}\n'
            f'Примечания: {order_info.ab}')

    return text.strip()


# краткий заказ строка
def get_short_order_row(order_info: db.OrderRow) -> str:
    return (f'<code>{order_info.n}</code>, <code>{order_info.o}</code>  {order_info.m} {order_info.x} '
            f'{order_info.f} {order_info.g}\n')
