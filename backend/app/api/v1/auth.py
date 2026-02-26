from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, hash_password, create_access_token
from app.api.deps import get_current_user
from app.models.staff import Staff
from app.schemas.auth import LoginRequest, TokenResponse, ChangePasswordRequest

router = APIRouter()


@router.post('/login', response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Staff).filter(Staff.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail='账号或密码错误')
    token = create_access_token({'sub': str(user.id)})
    return TokenResponse(
        token=token,
        id=user.id,
        username=user.username,
        name=user.name,
        role=user.role
    )


@router.post('/change-password')
def change_password(
    data: ChangePasswordRequest,
    current: Staff = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(data.old_password, current.password_hash):
        raise HTTPException(status_code=400, detail='当前密码错误')
    current.password_hash = hash_password(data.new_password)
    db.commit()
    return {'message': 'ok'}
