from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.staff import Staff
from app.services.ticket_service import TicketService

router = APIRouter()


@router.get('/today')
def get_today_stats(
    current: Staff = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return TicketService.get_today_stats(db, current.id)
