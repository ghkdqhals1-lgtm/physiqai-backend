from sqlalchemy import String, Integer, ForeignKey, Text, Date, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import date, datetime
import enum

from app.core.database import Base


class ExerciseType(str, enum.Enum):
    cardio = "cardio"
    strength = "strength"
    flexibility = "flexibility"
    sports = "sports"
    other = "other"


class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    exercise_type: Mapped[ExerciseType] = mapped_column(
        Enum(ExerciseType), default=ExerciseType.other, nullable=False
    )
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    calories_burned: Mapped[int | None] = mapped_column(Integer, nullable=True)
    workout_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="workout_logs")
