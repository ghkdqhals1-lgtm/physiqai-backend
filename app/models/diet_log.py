from sqlalchemy import String, Integer, Float, ForeignKey, Text, Date, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import date, datetime
import enum

from app.core.database import Base


class MealType(str, enum.Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"


class DietLog(Base):
    __tablename__ = "diet_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    meal_type: Mapped[MealType] = mapped_column(Enum(MealType), nullable=False)
    food_name: Mapped[str] = mapped_column(String(300), nullable=False)
    calories: Mapped[int | None] = mapped_column(Integer, nullable=True)
    protein_g: Mapped[float | None] = mapped_column(Float, nullable=True)
    carbs_g: Mapped[float | None] = mapped_column(Float, nullable=True)
    fat_g: Mapped[float | None] = mapped_column(Float, nullable=True)
    logged_at: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="diet_logs")
