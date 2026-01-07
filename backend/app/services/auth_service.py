from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemes.user_schema import User
from app.models.user_details import UserTable
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def add_user_db(user_data, db: AsyncSession):
    try:
        logger.info("Adding user to database")
        logger.info(user_data)
        new_user = UserTable(
            user_name=user_data["user_name"],
            password=user_data["password"],
            access_token=user_data["access_token"],
            instance_url=user_data["instance_url"],
            org_id=user_data["id"],
        )

        db.add(new_user)
        await db.commit()  # <-- MUST use await
        await db.refresh(new_user)  # <-- MUST use await
        logger.info("User Added")
        return new_user

    except Exception as e:
        logger.error("Error while adding user ", e)
        return f"Error while adding user {e}"
