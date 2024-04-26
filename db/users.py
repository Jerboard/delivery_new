from datetime import datetime
import typing as t
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_postgresql

from .base import METADATA, begin_connection


class UserRow(t.Protocol):
    id: int
    user_id: int
    full_name: str
    username: str
    status: str
    name: str


UserTable: sa.Table = sa.Table(
    "users",
    METADATA,

    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('user_id', sa.BigInteger, unique=True),
    sa.Column('full_name', sa.String(255)),
    sa.Column('username', sa.String(255)),
    sa.Column('status', sa.String(255)),
    sa.Column('name', sa.String(255)),
    sa.Column('company_id', sa.Integer)
)


# Добавляет пользователя
async def add_user(user_id: int, full_name: str, username: str, status: str) -> None:
    query = (
        sa_postgresql.insert(UserTable)
        .values(
            user_id=user_id,
            full_name=full_name,
            username=username,
            status=status,
        )
        .on_conflict_do_update(
            index_elements=[UserTable.c.user_id],
            set_={"full_name": full_name, 'username': username}
        )
    )
    async with begin_connection() as conn:
        await conn.execute(query)


# возвращает пользователя
async def get_user_info(user_id: int = None, name: str = None) -> UserRow:
    query = UserTable.select()

    if user_id:
        query = query.where(UserTable.c.user_id == user_id)
    if name:
        query = query.where(UserTable.c.name == name)

    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.first()


# возвращает пользователей
async def get_users(exc_user_id: int = None, company_id: str = None) -> tuple[UserRow]:
    query = UserTable.select()

    if exc_user_id:
        query = query.where(UserTable.c.user_id != exc_user_id)
    if company_id:
        query = query.where(UserTable.c.comp_id == company_id)

    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.all()


# обновляет данные пользователя
async def update_user_info(
        user_id: int,
        dlv_name: str = None,
        company_id: int = None,
) -> None:
    query = UserTable.update().where(UserTable.c.user_id == user_id)

    if dlv_name:
        query = query.values(name=dlv_name)

    if company_id:
        query = query.values(company_id=company_id)

    async with begin_connection() as conn:
        await conn.execute(query)
