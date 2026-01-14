# # db.py (or memory.py)

# import asyncio
# import sys
# from psycopg_pool import AsyncConnectionPool
# from psycopg.rows import dict_row
# from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

# # Windows fix (must be top-level)
# if sys.platform.startswith("win"):
#     asyncio.set_event_loop_policy(
#         asyncio.WindowsSelectorEventLoopPolicy()
#     )

# POOL = None
# CHECKPOINTER = None

# async def init_checkpointer():
#     global POOL, CHECKPOINTER

#     if CHECKPOINTER is not None:
#         return CHECKPOINTER

#     POOL = AsyncConnectionPool(
#         conninfo="postgres://postgres:1234@localhost:5432/checkpoints?sslmode=disable",
#         max_size=20,
#         kwargs={
#             "autocommit": True,
#             "prepare_threshold": 0,
#             "row_factory": dict_row,
#         },
#     )

#     # 🔑 IMPORTANT: AsyncPostgresSaver accepts a POOL, not a single conn
#     CHECKPOINTER = AsyncPostgresSaver(POOL)

#     return CHECKPOINTER


# post_memory.py

from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

POOL = None
CHECKPOINTER = None

async def init_checkpointer():
    global POOL, CHECKPOINTER

    if CHECKPOINTER is not None:
        return CHECKPOINTER

    POOL = AsyncConnectionPool(
        conninfo="postgres://postgres:1234@localhost:5432/checkpoints?sslmode=disable",
        max_size=20,
        kwargs={
            "autocommit": True,
            "prepare_threshold": 0,
            "row_factory": dict_row,
        },
        open=False,  # 🔑 IMPORTANT
    )

    await POOL.open()  # ✅ explicit open

    CHECKPOINTER = AsyncPostgresSaver(POOL)
    return CHECKPOINTER
