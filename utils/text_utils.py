import db


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
