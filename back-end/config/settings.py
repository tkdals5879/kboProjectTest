from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Baseball Info API"
    debug: bool = True
    db_url: str = "sqlite:///./baseball.db"  # 또는 PostgreSQL URL

    class Config:
        env_file = ".env"  # 이 파일에서 환경변수 읽기

settings = Settings() 