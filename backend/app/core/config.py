from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file = r"D:\SF-Dev-Agent\.env")
    SF_CLIENT_ID: str
    SF_CLIENT_SECRET: str
    SF_USERNAME: str
    SF_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
settings = Settings()
