from sqlmodel import SQLModel, create_engine, Session

DATABSE_URL = "sqlite:///book-exchange.db"

engine = create_engine(DATABSE_URL, echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    """Provides a new database session"""
    with Session(engine) as session:
        yield session