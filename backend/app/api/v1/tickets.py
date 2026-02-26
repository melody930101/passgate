from datetime import date
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.staff import Staff
from app.schemas.ticket import TicketCreate, VerifyRequest, VerifyResult
from app.services.ticket_service import TicketService

router = APIRouter()


@router.post('')
def create_ticket(
    data: TicketCreate,
    current: Staff = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return TicketService.create(db, data, current.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('')
def get_tickets(
    current: Staff = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    movie_id: int | None = None,
    status: str | None = None
):
    return TicketService.get_issue_history(db, current, page, page_size, movie_id, status)


@router.get('/check-unused')
def check_unused_tickets(
    current: Staff = Depends(get_current_user),
    db: Session = Depends(get_db),
    movie_id: int = Query(..., description='电影ID'),
    phone: str = Query(..., description='手机号')
):
    """检查同手机号+同电影是否有未核销票，供出票前 confirm 使用"""
    return TicketService.check_unused(db, movie_id, phone.strip())


@router.get('/check-history')
def get_check_history(
    current: Staff = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    movie_id: int | None = None,
    start_date: date | None = Query(None, description='筛选开始日期'),
    end_date: date | None = Query(None, description='筛选结束日期')
):
    return TicketService.get_check_history(db, current, page, page_size, movie_id, start_date, end_date)


@router.get('/{id}')
def get_ticket_detail(
    id: int,
    current: Staff = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return TicketService.get_detail(db, id, current)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/{id}/void')
def void_ticket(
    id: int,
    current: Staff = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        TicketService.void(db, id, current.id)
        return {'message': 'ok'}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/verify', response_model=VerifyResult)
def verify_ticket(
    data: VerifyRequest,
    current: Staff = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return TicketService.verify(db, data.ticket_code, current.id)
