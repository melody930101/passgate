from datetime import date, datetime
from pydantic import BaseModel


class TicketCreate(BaseModel):
    movie_id: int
    phone: str
    quantity: int = 1


class TicketResponse(BaseModel):
    id: int
    ticket_code: str
    movie_id: int
    movie_name: str
    phone: str
    quantity: int
    status: str
    issued_at: datetime
    issuer_name: str | None = None
    qr_base64: str | None = None
    end_date: date | None = None


class VerifyRequest(BaseModel):
    ticket_code: str


class VerifyResult(BaseModel):
    success: bool
    title: str
    details: list[dict]
