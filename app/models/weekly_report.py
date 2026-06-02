from sqlalchemy import Integer, Float, ForeignKey, Text, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import date, datetime

from app.core.database import Base


class WeeklyReport(Base):
    __tablename__ = "weekly_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    week_start: Mapped[date] = mapped_column(Date, nullable=False)
    week_end: Mapped[date] = mapped_column(Date, nullable=False)
    total_workout_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_workout_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    avg_sleep_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_daily_calories: Mapped[int | None] = mapped_column(Integer, nullable=True)
    report_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="weekly_reports")
