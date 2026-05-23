from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None


class UserMe(BaseModel):
    id: str
    email: str
    nombre: str
    apellido: str
    rol: str
    activo: bool

    class Config:
        from_attributes = True
