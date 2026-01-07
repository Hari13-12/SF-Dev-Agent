from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


def create_connection():
    username = settings.DB_USER
    password = settings.DB_PASS
    database_name = settings.DB_NAME
    host = settings.DB_HOST
    port = settings.DB_PORT  # usually 5432

    connection_url = (
        f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database_name}"
    )

    engine = create_async_engine(
        connection_url,
        echo=True,
        future=True,
    )
    return engine


# Create async engine
async_engine = create_connection()

# Create async session factory
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
