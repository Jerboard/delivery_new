import typing as t
import sqlalchemy as sa

from sqlalchemy.ext.asyncio import AsyncConnection

from init import ENGINE

METADATA = sa.MetaData ()


def begin_connection() -> t.AsyncContextManager [AsyncConnection]:
    ENGINE.connect ()
    return ENGINE.begin ()


async def init_models():
    async with ENGINE.begin () as conn:
        await conn.run_sync (METADATA.create_all)


async def create_trigger():
    async with ENGINE.begin() as conn:
        await conn.execute("""
            CREATE OR REPLACE FUNCTION update_orders_ggl_id()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.id := (SELECT COALESCE(MAX(id), 0) + 1 FROM orders_ggl);
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER orders_ggl_id_trigger
            BEFORE INSERT ON orders_ggl
            FOR EACH ROW
            EXECUTE PROCEDURE update_orders_ggl_id();
        """)

# второй вариант
'''
CREATE OR REPLACE FUNCTION update_orders_ggl_id()
RETURNS TRIGGER AS $$
DECLARE
    max_id BIGINT;
BEGIN
    SELECT MAX(id) INTO max_id FROM orders_ggl;
    NEW.id := COALESCE(max_id, 0) + 1;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
'''
