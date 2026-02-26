from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base


class Staff(Base):
    __tablename__ = 'staff'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    name = Column(String(64), nullable=False)
    role = Column(Enum('admin', 'staff'), nullable=False, default='staff')
    created_at = Column(DateTime, server_default=func.now())
