from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.models.staff import Staff

security = HTTPBearer(auto_error=False)


def get_current_user(
    cred: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db)
) -> Staff:
    if not cred:
        raise HTTPException(status_code=401, detail='未登录')
    payload = decode_token(cred.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail='Token 无效或已过期')
    uid = payload.get('sub')
    if not uid:
        raise HTTPException(status_code=401, detail='Token 无效')
    user = db.query(Staff).filter(Staff.id == int(uid)).first()
    if not user:
        raise HTTPException(status_code=401, detail='用户不存在')
    return user
