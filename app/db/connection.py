from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DB_FILE = 'app/db.db'


engine = create_engine(f"sqlite:///{DB_FILE}", connect_args={"check_same_thread": False})

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db_session():
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()