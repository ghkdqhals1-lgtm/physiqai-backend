from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import FitnessLevel, Goal


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    age: Optional[int] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    fitness_level: FitnessLevel = FitnessLevel.beginner
    goal: Goal = Goal.maintenance


class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    fitness_level: Optional[FitnessLevel] = None
    goal: Optional[Goal] = None


class UserResponse(BaseModel):
    id: int
    email: str
    name: Optional[str]
    age: Optional[int]
    weight_kg: Optional[float]
    height_cm: Optional[float]
    fitness_level: FitnessLevel
    goal: Goal
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
