from typing import Optional
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.deps import get_current_user_id
from app.models.diet_log import DietLog
from app.schemas.diet_log import DietLogCreate, DietLogUpdate, DietLogResponse

router = APIRouter()


@router.get("/", response_model=list[DietLogResponse])
async def list_logs(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    q = select(DietLog).where(DietLog.user_id == user_id)
    if date_from:
        q = q.where(DietLog.logged_at >= date_from)
    if date_to:
        q = q.where(DietLog.logged_at <= date_to)
    q = q.order_by(DietLog.logged_at.desc())

    result = await db.execute(q)
    return result.scalars().all()


@router.post("/", response_model=DietLogResponse, status_code=status.HTTP_201_CREATED)
async def create_log(
    data: DietLogCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    log = DietLog(**data.model_dump(), user_id=user_id)
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


@router.get("/{log_id}", response_model=DietLogResponse)
async def get_log(
    log_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(DietLog).where(DietLog.id == log_id, DietLog.user_id == user_id)
    )
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diet log not found")
    return log


@router.put("/{log_id}", response_model=DietLogResponse)
async def update_log(
    log_id: int,
    data: DietLogUpdate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(DietLog).where(DietLog.id == log_id, DietLog.user_id == user_id)
    )
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diet log not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(log, field, value)

    await db.commit()
    await db.refresh(log)
    return log


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_log(
    log_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(DietLog).where(DietLog.id == log_id, DietLog.user_id == user_id)
    )
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diet log not found")

    await db.delete(log)
    await db.commit()
