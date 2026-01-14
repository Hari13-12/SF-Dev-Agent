import asyncio, psycopg

async def test():
    try:
        await psycopg.AsyncConnection.connect(
            "postgresql://postgres:1234@localhost:5432/sqlagentcheckpoint"
        )
    except Exception as e:
        print(e)

asyncio.run(test())
