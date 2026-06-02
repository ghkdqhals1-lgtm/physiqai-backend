from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class InBodyCreate(BaseModel):
    weight_kg: float
    body_fat_percent: Optional[float] = None
    muscle_mass_kg: Optional[float] = None
    bmi: Optional[float] = None
    water_percent: Optional[float] = None
    bone_mass_kg: Optional[float] = None
    visceral_fat_level: Optional[int] = None
    measured_at: date


class InBodyUpdate(BaseModel):
    weight_kg: Optional[float] = None
    body_fat_percent: Optional[float] = None
    muscle_mass_kg: Optional[float] = None
    bmi: Optional[float] = None
    water_percent: Optional[float] = None
    bone_mass_kg: Optional[float] = None
    visceral_fat_level: Optional[int] = None
    measured_at: Optional[date] = None


class InBodyResponse(BaseModel):
    id: int
    user_id: int
    weight_kg: float
    body_fat_percent: Optional[float]
    muscle_mass_kg: Optional[float]
    bmi: Optional[float]
    water_percent: Optional[float]
    bone_mass_kg: Optional[float]
    visceral_fat_level: Optional[int]
    measured_at: date
    created_at: datetime

    class Config:
        from_attributes = True
