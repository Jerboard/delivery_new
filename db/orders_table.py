from datetime import datetime, date
import typing as tp

import sqlalchemy as sa

from .base import METADATA, begin_connection
from init import TZ
from enums.base_enum import SearchType, OrderStatus


class OrderRow(tp.Protocol):
    id: int
    b: str
    c: str
    d: str
    e: str
    f: str
    g: str
    h: str
    i: str
    j: str
    k: str
    l: str
    m: str
    n: str
    o: str
    p: str
    q: int
    r: int
    s: int
    clmn_t: int
    u: int
    v: int
    w: str
    x: str
    y: int
    z: str
    aa: str
    ab: str
    ac: str
    ad: str
    ae: str
    af: str
    ag: str
    ah: str
    updated: bool
    time_update: datetime
    type_update: str
    discount: int
    row_num: int


OrderTable: sa.Table = sa.Table(
    "orders_ggl",
    METADATA,

    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('b', sa.String(255)),
    sa.Column('c', sa.String(255)),
    sa.Column('d', sa.String(255)),
    sa.Column('e', sa.String(255)),
    sa.Column('f', sa.String(255)),
    sa.Column('g', sa.String(255)),
    sa.Column('h', sa.String(255)),
    sa.Column('i', sa.String(255)),
    sa.Column('j', sa.String(255)),
    sa.Column('k', sa.String(255)),
    sa.Column('l', sa.String(255)),
    sa.Column('m', sa.Text()),
    sa.Column('n', sa.String(255)),
    sa.Column('o', sa.String(255)),
    sa.Column('p', sa.Text),
    sa.Column('q', sa.Integer),
    sa.Column('r', sa.Integer),
    sa.Column('s', sa.Integer),
    sa.Column('clmn_t', sa.Integer),
    sa.Column('u', sa.Integer),
    sa.Column('v', sa.Integer),
    sa.Column('w', sa.String(255)),
    sa.Column('x', sa.Text),
    sa.Column('y', sa.Integer),
    sa.Column('z', sa.String(255)),
    sa.Column('aa', sa.String(255)),
    sa.Column('ab', sa.String(255)),
    sa.Column('ac', sa.String(255)),
    sa.Column('ad', sa.String(255)),
    sa.Column('ae', sa.String(255)),
    sa.Column('af', sa.String(255)),
    sa.Column('ag', sa.String(255)),
    sa.Column('ah', sa.String(255)),
    sa.Column('updated', sa.Boolean, default=True),
    sa.Column('time_update', sa.DateTime(timezone=True), default=datetime.now(TZ).replace(microsecond=0)),
    sa.Column('type_update', sa.String(255)),
    sa.Column('discount', sa.Integer(), default=0),
    sa.Column('row_num', sa.Integer()),
)


# добавляет строку
async def add_row(
    row_num: int,
    b: str,
    c: str,
    d: str,
    e: str,
    f: str,
    g: str,
    h: str,
    i: str,
    j: str,
    k: str,
    l: str,
    m: str,
    n: str,
    o: str,
    p: str,
    q: int,
    r: int,
    s: int,
    t: int,
    u: int,
    v: int,
    w: str,
    x: str,
    y: int,
    z: str,
    aa: str,
    ab: str,
    ac: str,
    ad: str,
    ae: str,
    af: str,
    ag: str,
    ah: str,
    type_update: str,
    updated: bool = False,
    empty_id: int = None
):
    query = OrderTable.insert().values(
        row_num=row_num,
        b=b,
        c=c,
        d=d,
        e=e,
        f=f,
        g=g,
        h=h,
        i=i,
        j=j,
        k=k,
        l=l,
        m=m,
        n=n,
        o=o,
        p=p,
        q=q,
        r=r,
        s=s,
        clmn_t=t,
        u=u,
        v=v,
        w=w,
        x=x,
        y=y,
        z=z,
        aa=aa,
        ab=ab,
        ac=ac,
        ad=ad,
        ae=ae,
        af=af,
        ag=ag,
        ah=ah,
        type_update=type_update,
        updated=updated
    )
    if empty_id:
        query = query.values(id=empty_id)
    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.inserted_primary_key[0]


# обновляет строку в таблице
# e - дата, f - курьер, g - статус, k - оператор, ab - примечание, f - курьер, y - скидка
async def update_row_google(
        order_id: int,
        update_row: bool = False,
        all_row: bool = False,
        b: str = None,
        c: str = None,
        d: str = None,
        e: str = None,
        f: str = None,
        g: str = None,
        h: str = None,
        i: str = None,
        j: str = None,
        k: str = None,
        l: str = None,
        m: str = None,
        n: str = None,
        o: str = None,
        p: str = None,
        q: int = None,
        r: int = None,
        s: int = None,
        t: int = None,
        u: int = None,
        v: int = None,
        w: str = None,
        x: str = None,
        y: int = None,
        z: str = None,
        aa: str = None,
        ab: str = None,
        ac: str = None,
        ad: str = None,
        ae: str = None,
        af: str = None,
        ag: str = None,
        ah: str = None,
        take_date: str = None,
        dlv_name: str = None,
        status: str = None,
        note: str = None,
        type_update: str = None,
        discount: int = None
):
    query = (OrderTable.update().where(OrderTable.c.id == order_id).
             values(updated=update_row,
                    time_update=datetime.now(TZ).replace(microsecond=0)))

    if take_date:
        query = query.values(e=take_date)
    if dlv_name:
        query = query.values(f=dlv_name)
    if status:
        query = query.values(g=status)
    if note:
        query = query.values(ab=note)
    if type_update:
        query = query.values(type_update=type_update)
    if discount:
        query = query.values(y=discount)
    if all_row:
        query = query.values(a=order_id, b=b, c=c, d=d, e=e, f=f, g=g, h=h, i=i, j=j, k=k, l=l, m=m, n=n, o=o, p=p,
                             q=q, r=r, s=s, clmn_t=t, u=u, v=v, w=w, x=x, y=y, z=z, aa=aa, ab=ab, ac=ac, ad=ad, ae=ae,
                             af=af, ag=ag, ah=ah)

    async with begin_connection() as conn:
        await conn.execute(query)


# возвращает строки таблицы
async def get_orders(
        dlv_name: str = None,
        get_active: bool = False,
        get_wait_update: bool = False,
        on_date: str = None) -> tuple[OrderRow]:
    query = OrderTable.select()

    if get_active:
        query = query.where(sa.or_(OrderTable.c.g == OrderStatus.NEW.value, OrderTable.c.g == OrderStatus.ACTIVE.value))
    elif get_wait_update:
        query = query.where (OrderTable.c.updated == False)

    if dlv_name:
        query = query.where(OrderTable.c.f == dlv_name)
    if on_date:
        query = query.where(OrderTable.c.e == on_date)
    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.all()


# возвращает одну строку таблицы
async def get_order(order_id: int = 0, for_update: bool = False) -> tp.Union[OrderRow, None]:
    query = OrderTable.select()

    if order_id:
        query = query.where (OrderTable.c.id == order_id)
    elif for_update:
        query = query.where(OrderTable.c.updated == False).order_by(OrderTable.c.time_update)

    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.first()


# показывает максимальный номер строки
async def get_max_row_num() -> int:
    query = sa.select(sa.func.max(OrderTable.c.row_num))
    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.scalar()


# удаляет заказ по id
async def delete_orders(order_id: int = 0, start_id: int = 0):
    query = OrderTable.delete()

    if order_id:
        query = query.where (OrderTable.c.id == order_id)
    elif start_id:
        query = query.where(OrderTable.c.id >= start_id)

    async with begin_connection() as conn:
        await conn.execute(query)


# поиск заказов
async def search_orders(search_query: str, search_on: str, comp: str = None) -> tuple[OrderRow]:
    query = OrderTable.select()

    if search_on == SearchType.PHONE:
        query = query.where(sa.or_(OrderTable.c.n.like(f'%{search_query}%'), OrderTable.c.o.like(f'%{search_query}%')))
    elif search_on == SearchType.NAME:
        query = query.where(OrderTable.c.m.like(f'%{search_query}%'))
    elif search_on == SearchType.METRO:
        query = query.where(OrderTable.c.w.like(f'%{search_query}%'))

    # if comp:
    #     query = query.where(OrderTable.c.ac == comp)

    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.all()


# количество заказов по статусам на руках и не принят
async def count_status_orders(dlv: str = 'all') -> tuple[int, int, int, int, int, int, int, int]:
    if dlv == 'all':
        query = sa.select(OrderTable.c.g, sa.func.count(OrderTable.c.g)).group_by(OrderTable.c.g)
        query2 = sa.select(sa.func.count(OrderTable.c.n)).where(OrderTable.c.n.isnot(None))

    else:
        query = (sa.select(OrderTable.c.g, sa.func.count(OrderTable.c.g))
                 .where(OrderTable.c.f == dlv,
                        OrderTable.c.c.isnot(None)).group_by(OrderTable.c.g))
        query2 = (sa.select(sa.func.count(OrderTable.c.n)).
                  where(OrderTable.c.n.isnot(None),
                        OrderTable.c.f == dlv,
                        OrderTable.c.c.isnot(None)))

    async with begin_connection() as conn:
        result = await conn.execute(query)
        group = result.all()

        result = await conn.execute(query2)
        len_res = result.scalar()

    all = int(len_res)

    free, busy, suc, approv, close, get, rework = 0, 0, 0, 0, 0, 0, 0
    for i in group:
        if i[0] == '':
            free = i[1]
        elif i[0] == 'на руках':
            busy = i[1]
        elif i[0] == 'доставлен':
            suc = i[1]
        elif i[0] == 'принят':
            approv = i[1]
        elif i[0] == 'отказ':
            close = i[1]
        elif i[0] == 'отправлен':
            get = i[1]
        elif i[0] == 'переделка':
            rework = i[1]

    return all, free, busy, suc, approv, close, get, rework
