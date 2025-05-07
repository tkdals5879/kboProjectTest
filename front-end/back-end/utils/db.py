from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.settings import settings  # 환경 설정에서 DB URL 가져옴

# 데이터베이스 연결 설정
SQLALCHEMY_DATABASE_URL = settings.db_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB 모델의 베이스 클래스
Base = declarative_base()

# 의존성 주입용 DB 세션 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 스케줄러용 세션 (yield 없이 직접 반환)
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()