"""
Quick migration to add missing columns.
Run with: python -m run_migration
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import asyncio
from sqlalchemy import text
from app.core.connect_db import async_engine


async def migrate():
    async with async_engine.begin() as conn:
        # Check current columns
        result = await conn.execute(
            text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users'
        """)
        )
        existing_columns = [row[0] for row in result]
        print(f"Existing columns: {existing_columns}")

        # Add missing columns
        if "accesstoken" not in existing_columns:
            await conn.execute(
                text("ALTER TABLE users ADD COLUMN accesstoken VARCHAR(500)")
            )
            print("✅ Added accesstoken")

        if "instance_url" not in existing_columns:
            await conn.execute(
                text("ALTER TABLE users ADD COLUMN instance_url VARCHAR(500)")
            )
            print("✅ Added instance_url")

        if "org_id" not in existing_columns:
            await conn.execute(text("ALTER TABLE users ADD COLUMN org_id VARCHAR(500)"))
            print("✅ Added org_id")

        # Rename username to user_name if needed
        if "username" in existing_columns and "user_name" not in existing_columns:
            await conn.execute(
                text("ALTER TABLE users RENAME COLUMN username TO user_name")
            )
            print("✅ Renamed username to user_name")

        print("\n✅ Migration complete!")


asyncio.run(migrate())
