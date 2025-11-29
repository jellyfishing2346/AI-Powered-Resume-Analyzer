"""
Job model for storing job descriptions and requirements.
"""

from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, SoftDeleteMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.match import Match

    from app.models.user import User


class Job(Base, TimestampMixin, SoftDeleteMixin):
    """Job description model with AI analysis."""

    __tablename__ = "jobs"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Foreign Keys
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Job Information
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    job_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # full-time, part-time, contract

    # Job Description
    raw_description: Mapped[str] = mapped_column(Text, nullable=False)
    cleaned_description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # AI-Extracted Requirements
    required_skills: Mapped[list | None] = mapped_column(JSON, nullable=True)
    preferred_skills: Mapped[list | None] = mapped_column(JSON, nullable=True)
    required_experience_years: Mapped[int | None] = mapped_column(Integer, nullable=True)
    required_education: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # AI Analysis
    key_responsibilities: Mapped[list | None] = mapped_column(JSON, nullable=True)
    benefits: Mapped[list | None] = mapped_column(JSON, nullable=True)
    salary_range: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # AI-Generated Summary
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Vector Embedding for Semantic Search
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(384),
        nullable=True,
    )

    # Status
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="jobs")
    matches: Mapped[list["Match"]] = relationship(
        "Match",
        back_populates="job",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Job {self.title} at {self.company}>"
