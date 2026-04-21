from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from resources.db_creds import MoviesDbCreds
from sqlalchemy.orm import Session

DB_URL = (
    f"postgresql+psycopg2://{MoviesDbCreds.USER}:{MoviesDbCreds.PASSWORD}"
    f"@{MoviesDbCreds.HOST}:{MoviesDbCreds.PORT}/{MoviesDbCreds.NAME}"
)

engine = create_engine(DB_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)


def get_db_session() -> Session:
    """Создает новую сессию БД"""
    return SessionLocal()
