"""
Resume model for storing resume data and analysis results.
"""

from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, SoftDeleteMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.match import Match

    from app.models.user import User


class Resume(Base, TimestampMixin, SoftDeleteMixin):
    """Resume model with AI analysis results."""

    __tablename__ = "resumes"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Foreign Keys
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # File Information
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)

    # Extracted Text
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    cleaned_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Basic Analysis
    word_count: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # AI Analysis Results (JSON)
    entities: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    skills: Mapped[list | None] = mapped_column(JSON, nullable=True)
    experience: Mapped[list | None] = mapped_column(JSON, nullable=True)
    education: Mapped[list | None] = mapped_column(JSON, nullable=True)
    contact_info: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # AI-Generated Summary
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Completeness & Quality Scores
    completeness_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    ats_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Vector Embedding for Semantic Search
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(384),  # Dimension for all-MiniLM-L6-v2
        nullable=True,
    )

    # Processing Status
    processing_status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
    )  # pending, processing, completed, failed

    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="resumes")
    matches: Mapped[list["Match"]] = relationship(
        "Match",
        back_populates="resume",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Resume {self.filename}>"
