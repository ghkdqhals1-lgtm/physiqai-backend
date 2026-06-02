from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.models.workout import ExerciseType


class WorkoutLogCreate(BaseModel):
    title: str
    notes: Optional[str] = None
    exercise_type: ExerciseType = ExerciseType.other
    duration_minutes: Optional[int] = None
    calories_burned: Optional[int] = None
    workout_date: date


class WorkoutLogUpdate(BaseModel):
    title: Optional[str] = None
    notes: Optional[str] = None
    exercise_type: Optional[ExerciseType] = None
    duration_minutes: Optional[int] = None
    calories_burned: Optional[int] = None
    workout_date: Optional[date] = None


class WorkoutLogResponse(BaseModel):
    id: int
    user_id: int
    title: str
    notes: Optional[str]
    exercise_type: ExerciseType
    duration_minutes: Optional[int]
    calories_burned: Optional[int]
    workout_date: date
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
