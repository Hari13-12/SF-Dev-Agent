"""
Migration script to add missing columns to the users table.
Run this once to update your database schema.
"""

import asyncio
from sqlalchemy import text
from app.core.connect_db import async_engine


async def add_missing_columns():
    """Add the missing columns to the users table."""

    async with async_engine.begin() as conn:
        try:
            # Add accesstoken column
            await conn.execute(
                text(
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS accesstoken VARCHAR(255)"
                )
            )
            print("✅ Added accesstoken column")

            # Add instance_url column
            await conn.execute(
                text(
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS instance_url VARCHAR(255)"
                )
            )
            print("✅ Added instance_url column")

            # Add org_id column
            await conn.execute(
                text("ALTER TABLE users ADD COLUMN IF NOT EXISTS org_id VARCHAR(255)")
            )
            print("✅ Added org_id column")

            # Rename username to user_name if it exists
            await conn.execute(
                text("ALTER TABLE users RENAME COLUMN username TO user_name")
            )
            print("✅ Renamed username to user_name")

        except Exception as e:
            if "already exists" in str(e) or "does not exist" in str(e):
                print(
                    f"⚠️  Column might already exist or username column doesn't exist: {e}"
                )
            else:
                raise e

    print("\n✅ Migration completed successfully!")


if __name__ == "__main__":
    asyncio.run(add_missing_columns())
