from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemes.user_schema import User
from app.services.auth_service import add_user_db
from app.core.db_session import get_db
from app.core.config import settings
import logging
import httpx

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


router = APIRouter(tags=["New_user"])


@router.post("/new_user")
async def add_new_user(user_data: User, db: AsyncSession = Depends(get_db)):
    url = f"https://login.salesforce.com/services/oauth2/token?grant_type=password&client_id={settings.SF_CLIENT_ID}&client_secret={settings.SF_CLIENT_SECRET}&username={settings.SF_USERNAME}&password={settings.SF_PASSWORD}"
    response = httpx.post(url)
    res = response.json()
    res["user_name"] = user_data.username
    res["password"] = user_data.password
    res = await add_user_db(res, db=db)
    return {"status": res}


