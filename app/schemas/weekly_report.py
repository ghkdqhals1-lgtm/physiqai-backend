from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import date, datetime


class WeeklyReportCreate(BaseModel):
    week_start: date
    week_end: date

    @model_validator(mode="after")
    def check_dates(self) -> "WeeklyReportCreate":
        if self.week_end <= self.week_start:
            raise ValueError("week_end must be after week_start")
        return self


class WeeklyReportUpdate(BaseModel):
    report_summary: Optional[str] = None
    total_workout_count: Optional[int] = None
    total_workout_minutes: Optional[int] = None
    avg_sleep_hours: Optional[float] = None
    avg_daily_calories: Optional[int] = None


class WeeklyReportResponse(BaseModel):
    id: int
    user_id: int
    week_start: date
    week_end: date
    total_workout_count: Optional[int]
    total_workout_minutes: Optional[int]
    avg_sleep_hours: Optional[float]
    avg_daily_calories: Optional[int]
    report_summary: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
