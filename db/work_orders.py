from datetime import datetime
import typing as t
import sqlalchemy as sa

from .base import METADATA, begin_connection
from db.orders_table import OrderRow, OrderTable


WorkTable: sa.Table = sa.Table(
    "work_orders",
    METADATA,

    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('user_id', sa.BigInteger),
    sa.Column('order_id', sa.Integer),
)


# возвращает заказы курьера
async def get_work_orders(user_id: int) -> tuple[OrderRow]:
    query = (
        sa.select (
            OrderTable.c.id,
            OrderTable.c.e,
            OrderTable.c.f,
            OrderTable.c.g,
            OrderTable.c.h,
            OrderTable.c.i,
            OrderTable.c.j,
            OrderTable.c.k,
            OrderTable.c.l,
            OrderTable.c.m,
            OrderTable.c.n,
            OrderTable.c.o,
            OrderTable.c.p,
            OrderTable.c.q,
            OrderTable.c.r,
            OrderTable.c.s,
            OrderTable.c.clmn_t,
            OrderTable.c.u,
            OrderTable.c.v,
            OrderTable.c.w,
            OrderTable.c.x,
            OrderTable.c.y,
            OrderTable.c.z,
            OrderTable.c.ab,
            OrderTable.c.ac,
        )
        .select_from (WorkTable.join (OrderTable, WorkTable.c.order_id == OrderTable.c.id)).
        where(WorkTable.c.user_id == user_id)
    )

    async with begin_connection () as conn:
        result = await conn.execute (query)

    return result.all ()


# возвращает заказы курьера
async def get_statistic_dlv(user_id: int) -> list[tuple]:
    query = (
        sa.select (
            OrderTable.c.g,
            sa.func.count ().label ('status_count')
        )
        .select_from (WorkTable.join (OrderTable, WorkTable.c.order_id == OrderTable.c.id)).
        where(WorkTable.c.user_id == user_id).
        group_by(OrderTable.c.g)
    )

    async with begin_connection () as conn:
        result = await conn.execute (query)

    return result.all ()


# добавляет заказ
async def add_work_order(user_id: int, order_id: int) -> None:
    query = WorkTable.insert().values(user_id=user_id, order_id=order_id)
    async with begin_connection() as conn:
        await conn.execute(query)


# добавляет заказ
async def update_work_order(order_id: int, user_id: int) -> None:
    query = WorkTable.update().where(WorkTable.c.order_id == order_id).values(user_id=user_id)
    async with begin_connection() as conn:
        await conn.execute(query)


# добавляет заказ
async def delete_work_order(order_id: int = None, user_id: int = None) -> None:
    if order_id:
        query = WorkTable.delete().where(WorkTable.c.order_id == order_id)
    elif user_id:
        query = WorkTable.delete().where(WorkTable.c.user_id == user_id)
    else:
        return
    async with begin_connection() as conn:
        await conn.execute(query)
