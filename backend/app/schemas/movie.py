from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class MovieCreate(BaseModel):
    name: str
    start_date: date
    end_date: date
    price: Decimal | None = None
    remark: str | None = None


class MovieUpdate(BaseModel):
    name: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    price: Decimal | None = None
    remark: str | None = None


class MovieResponse(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    price: Decimal | None
    remark: str | None
    is_active: int

    class Config:
        from_attributes = True
