from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    reports: Mapped[list["Report"]] = relationship(back_populates="agent")


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    agent_id: Mapped[int] = mapped_column(ForeignKey("agents.id"), nullable=False)

    address: Mapped[str] = mapped_column(String(500), nullable=False)
    landmark: Mapped[str] = mapped_column(String(500), default="")
    client_code: Mapped[str] = mapped_column(String(100), default="")
    last_trade_agent_visit: Mapped[str] = mapped_column(String(100), default="")
    stand_code: Mapped[str] = mapped_column(String(100), default="")
    client_comment: Mapped[str] = mapped_column(Text, default="")
    conclusion: Mapped[str] = mapped_column(Text, default="")

    rm_info: Mapped[str] = mapped_column(Text, default="")
    resolution_date: Mapped[str] = mapped_column(String(100), default="")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    agent: Mapped["Agent"] = relationship(back_populates="reports")
    photos: Mapped[list["ReportPhoto"]] = relationship(
        back_populates="report",
        cascade="all, delete-orphan"
    )


class ReportPhoto(Base):
    __tablename__ = "report_photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"), nullable=False)
    photo_type: Mapped[str] = mapped_column(String(50), nullable=False)
    photo_link: Mapped[str] = mapped_column(Text, default="")

    report: Mapped["Report"] = relationship(back_populates="photos")