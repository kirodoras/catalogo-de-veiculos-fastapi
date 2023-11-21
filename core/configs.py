from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv('DB_URL')

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = db_url

    class Config:
        case_sensitive = True


settings: Settings = Settings()
