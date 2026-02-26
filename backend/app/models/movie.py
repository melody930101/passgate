from sqlalchemy import Column, Integer, String, Date, Numeric, SmallInteger, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    price = Column(Numeric(10, 2), nullable=True)
    remark = Column(String(200), nullable=True)
    is_active = Column(SmallInteger, default=1)
    created_by = Column(Integer, ForeignKey('staff.id'), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
