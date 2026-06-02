from typing import Optional
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.deps import get_current_user_id
from app.models.workout import WorkoutLog
from app.schemas.workout import WorkoutLogCreate, WorkoutLogUpdate, WorkoutLogResponse

router = APIRouter()


@router.get("/", response_model=list[WorkoutLogResponse])
async def list_logs(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    q = select(WorkoutLog).where(WorkoutLog.user_id == user_id)
    if date_from:
        q = q.where(WorkoutLog.workout_date >= date_from)
    if date_to:
        q = q.where(WorkoutLog.workout_date <= date_to)
    q = q.order_by(WorkoutLog.workout_date.desc())

    result = await db.execute(q)
    return result.scalars().all()


@router.post("/", response_model=WorkoutLogResponse, status_code=status.HTTP_201_CREATED)
async def create_log(
    data: WorkoutLogCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    log = WorkoutLog(**data.model_dump(), user_id=user_id)
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


@router.get("/{log_id}", response_model=WorkoutLogResponse)
async def get_log(
    log_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(WorkoutLog).where(WorkoutLog.id == log_id, WorkoutLog.user_id == user_id)
    )
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout log not found")
    return log


@router.put("/{log_id}", response_model=WorkoutLogResponse)
async def update_log(
    log_id: int,
    data: WorkoutLogUpdate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(WorkoutLog).where(WorkoutLog.id == log_id, WorkoutLog.user_id == user_id)
    )
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout log not found")

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
        select(WorkoutLog).where(WorkoutLog.id == log_id, WorkoutLog.user_id == user_id)
    )
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout log not found")

    await db.delete(log)
    await db.commit()
