from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@localhost/sensor_data"  # Update with your credentials

# SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    from .models import Base
    print("Initiating db connection")
    Base.metadata.create_all(bind=engine)
