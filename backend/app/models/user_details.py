from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    access_token = Column(String(100), unique=True, nullable=False)
    instance_url = Column(String(100), unique=True, nullable=False)
    org_id = Column(String(100), unique=True, nullable=False)
