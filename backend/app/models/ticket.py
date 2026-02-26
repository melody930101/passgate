from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_code = Column(String(32), unique=True, nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    phone = Column(String(20), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    status = Column(Enum('unused', 'used', 'voided'), nullable=False, default='unused')
    issuer_id = Column(Integer, ForeignKey('staff.id'), nullable=False)
    issued_at = Column(DateTime, server_default=func.now())
    checker_id = Column(Integer, ForeignKey('staff.id'), nullable=True)
    checked_at = Column(DateTime, nullable=True)
    voided_by = Column(Integer, ForeignKey('staff.id'), nullable=True)
    voided_at = Column(DateTime, nullable=True)
