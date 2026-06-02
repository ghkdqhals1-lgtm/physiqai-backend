from typing import Optional
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.deps import get_current_user_id
from app.models.sleep_log import SleepLog
from app.schemas.sleep_log import SleepLogCreate, SleepLogUpdate, SleepLogResponse

router = APIRouter()


@router.get("/", response_model=list[SleepLogResponse])
async def list_logs(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    q = select(SleepLog).where(SleepLog.user_id == user_id)
    if date_from:
        q = q.where(SleepLog.sleep_date >= date_from)
    if date_to:
        q = q.where(SleepLog.sleep_date <= date_to)
    q = q.order_by(SleepLog.sleep_date.desc())

    result = await db.execute(q)
    return result.scalars().all()


@router.post("/", response_model=SleepLogResponse, status_code=status.HTTP_201_CREATED)
async def create_log(
    data: SleepLogCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    duration = (data.sleep_end - data.sleep_start).total_seconds() / 3600
    log = SleepLog(
        **data.model_dump(),
        user_id=user_id,
        duration_hours=round(duration, 2),
        sleep_date=data.sleep_start.date(),
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


@router.get("/{log_id}", response_model=SleepLogResponse)
async def get_log(
    log_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(SleepLog).where(SleepLog.id == log_id, SleepLog.user_id == user_id)
    )
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sleep log not found")
    return log


@router.put("/{log_id}", response_model=SleepLogResponse)
async def update_log(
    log_id: int,
    data: SleepLogUpdate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(SleepLog).where(SleepLog.id == log_id, SleepLog.user_id == user_id)
    )
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sleep log not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(log, field, value)

    # Recalculate duration if times changed
    if data.sleep_start or data.sleep_end:
        start = data.sleep_start or log.sleep_start
        end = data.sleep_end or log.sleep_end
        if end > start:
            log.duration_hours = round((end - start).total_seconds() / 3600, 2)
            log.sleep_date = start.date()

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
        select(SleepLog).where(SleepLog.id == log_id, SleepLog.user_id == user_id)
    )
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sleep log not found")

    await db.delete(log)
    await db.commit()
