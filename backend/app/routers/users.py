from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate, UserOut
from app.auth.utils import hash_password
from app.utils import log_auditoria

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserOut])
async def list_users(
    activo: Optional[bool] = True,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_admin),
):
    q = select(User)
    if activo is not None:
        q = q.where(User.activo == activo)
    if search:
        q = q.where(
            (User.email.ilike(f"%{search}%"))
            | (User.nombre.ilike(f"%{search}%"))
            | (User.apellido.ilike(f"%{search}%"))
        )
    q = q.offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_admin),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_admin),
):
    # Check email uniqueness
    existing = await db.execute(select(User).where(User.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=data.email,
        nombre=data.nombre,
        apellido=data.apellido,
        password_hash=hash_password(data.password),
        rol=data.rol,
    )
    db.add(user)
    await db.flush()

    await log_auditoria(
        db=db,
        tabla="users",
        registro_id=user.id,
        accion="CREATE",
        usuario_id=current_user.id,
        usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
        descripcion=f"Usuario creado: {user.email}",
    )

    await db.commit()
    await db.refresh(user)
    return user


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: str,
    data: UserUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_admin),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, new_val in update_data.items():
        if field == "password":
            old_val = "***"
            new_val_hashed = hash_password(new_val)
            setattr(user, "password_hash", new_val_hashed)
            await log_auditoria(
                db=db,
                tabla="users",
                registro_id=user_id,
                accion="UPDATE",
                campo="password_hash",
                valor_anterior=old_val,
                valor_nuevo="***",
                usuario_id=current_user.id,
                usuario_email=current_user.email,
                ip=request.client.host if request.client else None,
            )
        else:
            old_val = str(getattr(user, field, None))
            setattr(user, field, new_val)
            await log_auditoria(
                db=db,
                tabla="users",
                registro_id=user_id,
                accion="UPDATE",
                campo=field,
                valor_anterior=old_val,
                valor_nuevo=str(new_val),
                usuario_id=current_user.id,
                usuario_email=current_user.email,
                ip=request.client.host if request.client else None,
            )

    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user(
    user_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_admin),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.activo = False
    await log_auditoria(
        db=db,
        tabla="users",
        registro_id=user_id,
        accion="DEACTIVATE",
        usuario_id=current_user.id,
        usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
    )
    await db.commit()
