from pydantic_settings import BaseSettings
from pydantic import AnyUrl

class Settings(BaseSettings):
    DATABASE_URL: AnyUrl
    PRODUCTION: bool
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_BUCKET: str
    SUPABASE_BUCKET_RESUME: str
    ADMIN_USER_NAME: str
    ADMIN_PASSWORD: str
    RESEND_API_KEY: str
    

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()