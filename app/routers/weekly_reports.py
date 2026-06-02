from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.deps import get_current_user_id
from app.models.weekly_report import WeeklyReport
from app.models.workout import WorkoutLog
from app.models.sleep_log import SleepLog
from app.models.diet_log import DietLog
from app.schemas.weekly_report import WeeklyReportCreate, WeeklyReportUpdate, WeeklyReportResponse

router = APIRouter()


@router.get("/", response_model=list[WeeklyReportResponse])
async def list_reports(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(WeeklyReport)
        .where(WeeklyReport.user_id == user_id)
        .order_by(WeeklyReport.week_start.desc())
    )
    return result.scalars().all()


@router.post("/", response_model=WeeklyReportResponse, status_code=status.HTTP_201_CREATED)
async def generate_report(
    data: WeeklyReportCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    w_result = await db.execute(
        select(
            func.count(WorkoutLog.id).label("cnt"),
            func.coalesce(func.sum(WorkoutLog.duration_minutes), 0).label("total_min"),
        ).where(
            WorkoutLog.user_id == user_id,
            WorkoutLog.workout_date.between(data.week_start, data.week_end),
        )
    )
    w = w_result.one()

    s_result = await db.execute(
        select(func.avg(SleepLog.duration_hours)).where(
            SleepLog.user_id == user_id,
            SleepLog.sleep_date.between(data.week_start, data.week_end),
        )
    )
    avg_sleep = s_result.scalar()

    d_result = await db.execute(
        select(func.sum(DietLog.calories)).where(
            DietLog.user_id == user_id,
            DietLog.logged_at.between(data.week_start, data.week_end),
        )
    )
    total_cal = d_result.scalar()
    days = (data.week_end - data.week_start).days or 1

    report = WeeklyReport(
        user_id=user_id,
        week_start=data.week_start,
        week_end=data.week_end,
        total_workout_count=w.cnt,
        total_workout_minutes=w.total_min,
        avg_sleep_hours=round(avg_sleep, 2) if avg_sleep else None,
        avg_daily_calories=int(total_cal / days) if total_cal else None,
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report


@router.get("/{report_id}", response_model=WeeklyReportResponse)
async def get_report(
    report_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(WeeklyReport).where(WeeklyReport.id == report_id, WeeklyReport.user_id == user_id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return report


@router.put("/{report_id}", response_model=WeeklyReportResponse)
async def update_report(
    report_id: int,
    data: WeeklyReportUpdate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(WeeklyReport).where(WeeklyReport.id == report_id, WeeklyReport.user_id == user_id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(report, field, value)

    await db.commit()
    await db.refresh(report)
    return report


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    report_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(WeeklyReport).where(WeeklyReport.id == report_id, WeeklyReport.user_id == user_id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    await db.delete(report)
    await db.commit()
