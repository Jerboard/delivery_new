from random import choice

import db
from enums import UserRole


# обрабатывает строку с числом, возвращает число, если строка содержит число, иначе возвращает 0
def hand_digit(values: str) -> int:
    if not values == '' or values == ' ':
        digit = 0
    else:
        chars = [' ', '\xa0']
        values = values.translate(str.maketrans('', '', ''.join(chars)))
        digit = int(values) if str(values).isdigit() else 0

    return digit


# функция генерирует случайный из латинских букв и цифр
def get_random_code():
    return ''.join([choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(8)])


# выдаёт словарь для курьеров имя: id
async def get_dlv_name_dict() -> dict[str: int]:
    users = await db.get_users(role=UserRole.DLV.value)
    return {user.name: user.user_id for user in users}


# выдаёт словарь для курьеров имя: id
async def get_work_orders_list() -> list[int]:
    orders = await db.get_work_orders()
    return [order.id for order in orders]


# считает стоимость
def get_order_cost(order: db.OrderRow, with_t: bool = False) -> int:
    prepay = order.u + order.v
    if with_t:
        return (0 if order.q == 0 and prepay != 0 else order.q + order.r + order.s - order.y) + order.clmn_t
    else:
        return 0 if order.q == 0 and prepay != 0 else order.q + order.r + order.s - order.y


# async def start_test_work():
#     await db.delete_work_order()
#
#     users = await db.get_users(role=UserRole.DLV.value)
#
#     for user in users:
#         orders = await db.get_orders(dlv_name=user.name, get_active=True)
#
#         for order in orders:
#             await db.add_work_order(user_id=user.user_id, order_id=order.id)
