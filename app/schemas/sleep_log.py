from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import date, datetime


class SleepLogCreate(BaseModel):
    sleep_start: datetime
    sleep_end: datetime
    quality: Optional[int] = None
    notes: Optional[str] = None

    @model_validator(mode="after")
    def check_end_after_start(self) -> "SleepLogCreate":
        if self.sleep_end <= self.sleep_start:
            raise ValueError("sleep_end must be after sleep_start")
        return self

    @field_validator("quality")
    @classmethod
    def check_quality_range(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not (1 <= v <= 10):
            raise ValueError("quality must be between 1 and 10")
        return v


class SleepLogUpdate(BaseModel):
    sleep_start: Optional[datetime] = None
    sleep_end: Optional[datetime] = None
    quality: Optional[int] = None
    notes: Optional[str] = None

    @field_validator("quality")
    @classmethod
    def check_quality_range(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not (1 <= v <= 10):
            raise ValueError("quality must be between 1 and 10")
        return v


class SleepLogResponse(BaseModel):
    id: int
    user_id: int
    sleep_start: datetime
    sleep_end: datetime
    duration_hours: Optional[float]
    quality: Optional[int]
    notes: Optional[str]
    sleep_date: date
    created_at: datetime

    class Config:
        from_attributes = True
