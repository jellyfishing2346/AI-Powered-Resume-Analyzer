"""
Match model for storing resume-job matching results.
"""

from typing import TYPE_CHECKING

from sqlalchemy import JSON, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.job import Job
    from app.models.resume import Resume


class Match(Base, TimestampMixin):
    """Resume-Job matching results with detailed scoring."""

    __tablename__ = "matches"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Foreign Keys
    resume_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    job_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Overall Score
    overall_score: Mapped[float] = mapped_column(Float, nullable=False, index=True)

    # Component Scores
    semantic_similarity: Mapped[float | None] = mapped_column(Float, nullable=True)
    skill_match_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    experience_match_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    education_match_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Detailed Analysis
    matched_skills: Mapped[list | None] = mapped_column(JSON, nullable=True)
    missing_skills: Mapped[list | None] = mapped_column(JSON, nullable=True)
    skill_gaps: Mapped[list | None] = mapped_column(JSON, nullable=True)

    # AI-Generated Analysis
    ai_explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    strengths: Mapped[list | None] = mapped_column(JSON, nullable=True)
    weaknesses: Mapped[list | None] = mapped_column(JSON, nullable=True)
    recommendations: Mapped[list | None] = mapped_column(JSON, nullable=True)

    # Ranking
    rank: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Status
    status: Mapped[str] = mapped_column(
        String(50),
        default="active",
        nullable=False,
    )  # active, archived, rejected

    # Relationships
    resume: Mapped["Resume"] = relationship("Resume", back_populates="matches")
    job: Mapped["Job"] = relationship("Job", back_populates="matches")

    def __repr__(self) -> str:
        return f"<Match resume={self.resume_id} job={self.job_id} score={self.overall_score:.2f}>"
