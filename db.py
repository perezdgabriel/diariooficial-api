from sqlalchemy import create_engine, Column, BigInteger, Date, Text, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class NormaGeneralDB(Base):
    __tablename__ = "normas_generales"

    id = Column(BigInteger, primary_key=True)
    date = Column(Date, nullable=False)
    edition = Column(Text)
    branch = Column(Text)
    ministry = Column(Text)
    organ = Column(Text)
    title = Column(Text, nullable=False)
    pdf_url = Column(Text)
    cve = Column(Text, unique=True, nullable=False)
    created_at = Column(Text)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
