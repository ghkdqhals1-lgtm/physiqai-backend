from sqlalchemy import Integer, Float, ForeignKey, Text, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import date, datetime

from app.core.database import Base


class SleepLog(Base):
    __tablename__ = "sleep_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    sleep_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    sleep_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    quality: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    sleep_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="sleep_logs")
