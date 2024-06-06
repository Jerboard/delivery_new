from datetime import datetime, date
import typing as tp

import sqlalchemy as sa

from config import Config
from .base import METADATA, begin_connection, ENGINE
from db.users import UserTable
from enums.base_enum import SearchType, OrderStatus, TypeOrderUpdate, active_status_list


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
    user_id: int
    phone: str
    company: str


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
    sa.Column('time_update', sa.DateTime(timezone=True), default=datetime.now(Config.tz)),
    sa.Column('type_update', sa.String(255)),
    sa.Column('discount', sa.Integer(), default=0),
    sa.Column('row_num', sa.Integer()),
)


# Индексируем таблицу
async def index_table():
    idx = sa.Index('idx_id', OrderTable.c.user_id)
    idx.create(ENGINE)


# синхронезирует автоинкримент с последним id
async def syncing_id():
    async with begin_connection() as conn:
        await conn.execute (sa.text ("SELECT setval('orders_ggl_id_seq', (SELECT MAX(id) FROM orders_ggl));"))


# добавляет строку
async def add_row(
    row_num: int,
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
    q: int = 0,
    r: int = 0,
    s: int = 0,
    t: int = 0,
    u: int = 0,
    v: int = 0,
    w: str = None,
    x: str = None,
    y: int = 0,
    z: str = None,
    aa: str = None,
    ab: str = None,
    ac: str = None,
    ad: str = None,
    ae: str = None,
    af: str = None,
    ag: str = None,
    ah: str = None,
    type_update: str = None,
    updated: bool = False,
    entry_id: int = None
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
        time_update=datetime.now(Config.tz),
        updated=updated
    )
    if entry_id:
        query = query.values(id=entry_id)
    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.inserted_primary_key[0]


# обновляет строку в таблице
# e - дата, f - курьер, g - статус, k - оператор, ab - примечание, f - курьер, y - скидка
async def update_row_google(
        order_id: int,
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
        update_row: bool = False,
        all_row: bool = False,
        take_date: str = None,
        dlv_name: str = None,
        status: str = None,
        note: str = None,
        type_update: str = None,
        discount: int = None,
        cost_delivery: int = None,
        letter: str = None,
):
    query = (OrderTable.update().where(OrderTable.c.id == order_id).
             values(updated=update_row,
                    time_update=datetime.now(Config.tz)))

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
    if cost_delivery:
        query = query.values(clmn_t=cost_delivery)
    if letter:
        query = query.values(d=letter) if letter != 'del' else query.values(d='')
    if all_row:
        query = query.values(b=b, c=c, d=d, e=e, f=f, g=g, h=h, i=i, j=j, k=k, l=l, m=m, n=n, o=o, p=p,
                             q=q, r=r, s=s, clmn_t=t, u=u, v=v, w=w, x=x, y=y, z=z, aa=aa, ab=ab, ac=ac, ad=ad, ae=ae,
                             af=af, ag=ag, ah=ah)

    async with begin_connection() as conn:
        await conn.execute(query)


# обновляет несколько заказов
async def update_multi_orders(
        date_str: str = None,
        type_update: str = TypeOrderUpdate.EDIT.value
) -> None:
    if type_update == TypeOrderUpdate.UP_DATE.value:
        query = OrderTable.update().where(OrderTable.c.g.in_ (active_status_list)).values(
            updated=False,
            time_update=datetime.now(Config.tz),
            type_update=type_update,
            e=date_str,
            d=None
        )
    elif type_update == TypeOrderUpdate.NOT_COME.value:
        query = OrderTable.update ().where (OrderTable.c.g == OrderStatus.NOT_COME.value).values (
            updated=False,
            time_update=datetime.now (Config.tz),
            type_update=type_update,
            g=OrderStatus.ACTIVE.value,
            letter=''
        )

    async with begin_connection() as conn:
        await conn.execute(query)


# возвращает строки таблицы
async def get_orders(
        user_id: int = None,
        dlv_name: str = None,
        get_active: bool = False,
        get_new: bool = False,
        get_wait_update: bool = False,
        on_date: str = None,
        search_query: str = None,
        search_on: str = None
) -> tuple[OrderRow]:
    query = sa.select(
        OrderTable.c.id,
        OrderTable.c.b,
        OrderTable.c.c,
        OrderTable.c.d,
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
        OrderTable.c.aa,
        OrderTable.c.ab,
        OrderTable.c.ac,
        OrderTable.c.ad,
        OrderTable.c.ae,
        OrderTable.c.af,
        OrderTable.c.ag,
        OrderTable.c.ah,
        OrderTable.c.updated,
        OrderTable.c.time_update,
        OrderTable.c.type_update,
        OrderTable.c.discount,
        OrderTable.c.row_num,
        OrderTable.c.id,
        UserTable.c.user_id,
        UserTable.c.phone,
        UserTable.c.company,
    ).select_from (OrderTable.join (UserTable, OrderTable.c.f == UserTable.c.name, isouter=True))

    if get_active:
        # query = query.where(
        #     sa.or_(OrderTable.c.g == OrderStatus.ACTIVE_TAKE.value, OrderTable.c.g == OrderStatus.ACTIVE.value)
        # )
        query = query.where (OrderTable.c.g.in_ (active_status_list))
    elif get_new:
        query = query.where(sa.and_(OrderTable.c.g == OrderStatus.NEW.value, OrderTable.c.i.isnot(None)))
    elif get_wait_update:
        query = query.where (OrderTable.c.updated.is_(False))

    if dlv_name:
        query = query.where(OrderTable.c.f == dlv_name)
    elif user_id:
        query = query.where(UserTable.c.user_id == user_id)
    if on_date:
        query = query.where(OrderTable.c.e == on_date)

    if search_on == SearchType.PHONE:
        query = query.where(sa.or_(OrderTable.c.n.like(f'%{search_query}%'), OrderTable.c.o.like(f'%{search_query}%')))
    elif search_on == SearchType.NAME:
        query = query.where(OrderTable.c.m.like(f'%{search_query}%'))
    elif search_on == SearchType.METRO:
        query = query.where(OrderTable.c.w.like(f'%{search_query}%'))

    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.all()


# возвращает одну строку таблицы
async def get_order(order_id: int = 0, for_update: bool = False) -> tp.Union[OrderRow, None]:
    query = sa.select (
        OrderTable.c.id,
        OrderTable.c.b,
        OrderTable.c.c,
        OrderTable.c.d,
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
        OrderTable.c.aa,
        OrderTable.c.ab,
        OrderTable.c.ac,
        OrderTable.c.ad,
        OrderTable.c.ae,
        OrderTable.c.af,
        OrderTable.c.ag,
        OrderTable.c.ah,
        OrderTable.c.updated,
        OrderTable.c.time_update,
        OrderTable.c.type_update,
        OrderTable.c.discount,
        OrderTable.c.row_num,
        OrderTable.c.id,
        UserTable.c.user_id,
        UserTable.c.phone,
    ).select_from (OrderTable.join (UserTable, OrderTable.c.f == UserTable.c.name, isouter=True))

    if order_id:
        query = query.where (OrderTable.c.id == order_id)
    elif for_update:
        query = query.where(OrderTable.c.updated.is_(False)).order_by(OrderTable.c.time_update)

    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.first()


# показывает максимальный номер строки
async def get_max_row_num() -> int:
    query = sa.select(sa.func.max(OrderTable.c.row_num))
    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.scalar()


# очищает таблицу
async def delete_orders():
    query = OrderTable.delete()
    async with begin_connection() as conn:
        await conn.execute(query)


# поиск заказов
# async def search_orders(search_query: str, search_on: str, comp: str = None) -> tuple[OrderRow]:
#     query = OrderTable.select()
#
#     if search_on == SearchType.PHONE:
#         query = query.where(sa.or_(OrderTable.c.n.like(f'%{search_query}%'), OrderTable.c.o.like(f'%{search_query}%')))
#     elif search_on == SearchType.NAME:
#         query = query.where(OrderTable.c.m.like(f'%{search_query}%'))
#     elif search_on == SearchType.METRO:
#         query = query.where(OrderTable.c.w.like(f'%{search_query}%'))
#
#     # if comp:
#     #     query = query.where(OrderTable.c.ac == comp)
#
#     async with begin_connection() as conn:
#         result = await conn.execute(query)
#     return result.all()


# статистика заказов
async def get_orders_statistic(dlv_name: str = None, on_date: str = None):
    query = (OrderTable.select().
             with_only_columns(OrderTable.c.g, sa.func.count().label('status_count')).
             group_by(OrderTable.c.g))

    if dlv_name:
        query = query.where(OrderTable.c.f == dlv_name)
    if on_date:
        query = query.where(OrderTable.c.e == on_date)

    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.all()
