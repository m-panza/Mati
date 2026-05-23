from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    nombre: str
    apellido: str
    password: str
    rol: str = "operador"


class UserUpdate(BaseModel):
    email: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    password: Optional[str] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None


class UserOut(BaseModel):
    id: str
    email: str
    nombre: str
    apellido: str
    rol: str
    activo: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
