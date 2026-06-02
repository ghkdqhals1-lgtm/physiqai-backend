from sqlalchemy import String, Integer, Float, Enum, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
import enum
from datetime import datetime

from app.core.database import Base


class FitnessLevel(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class Goal(str, enum.Enum):
    weight_loss = "weight_loss"
    muscle_gain = "muscle_gain"
    maintenance = "maintenance"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    height_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    fitness_level: Mapped[FitnessLevel] = mapped_column(
        Enum(FitnessLevel), default=FitnessLevel.beginner, nullable=False
    )
    goal: Mapped[Goal] = mapped_column(Enum(Goal), default=Goal.maintenance, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    inbody_records: Mapped[list["InBodyRecord"]] = relationship(
        "InBodyRecord", back_populates="user", cascade="all, delete-orphan"
    )
    workout_logs: Mapped[list["WorkoutLog"]] = relationship(
        "WorkoutLog", back_populates="user", cascade="all, delete-orphan"
    )
    diet_logs: Mapped[list["DietLog"]] = relationship(
        "DietLog", back_populates="user", cascade="all, delete-orphan"
    )
    sleep_logs: Mapped[list["SleepLog"]] = relationship(
        "SleepLog", back_populates="user", cascade="all, delete-orphan"
    )
    weekly_reports: Mapped[list["WeeklyReport"]] = relationship(
        "WeeklyReport", back_populates="user", cascade="all, delete-orphan"
    )
