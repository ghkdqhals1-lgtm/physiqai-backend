from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.models.diet_log import MealType


class DietLogCreate(BaseModel):
    meal_type: MealType
    food_name: str
    calories: Optional[int] = None
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fat_g: Optional[float] = None
    logged_at: date
    notes: Optional[str] = None


class DietLogUpdate(BaseModel):
    meal_type: Optional[MealType] = None
    food_name: Optional[str] = None
    calories: Optional[int] = None
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fat_g: Optional[float] = None
    logged_at: Optional[date] = None
    notes: Optional[str] = None


class DietLogResponse(BaseModel):
    id: int
    user_id: int
    meal_type: MealType
    food_name: str
    calories: Optional[int]
    protein_g: Optional[float]
    carbs_g: Optional[float]
    fat_g: Optional[float]
    logged_at: date
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
