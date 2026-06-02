from sqlalchemy import Integer, Float, ForeignKey, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import date, datetime

from app.core.database import Base


class InBodyRecord(Base):
    __tablename__ = "inbody_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False)
    body_fat_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    muscle_mass_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    bmi: Mapped[float | None] = mapped_column(Float, nullable=True)
    water_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    bone_mass_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    visceral_fat_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    measured_at: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="inbody_records")
