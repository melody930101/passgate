from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    token: str
    id: int
    username: str
    name: str
    role: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
