
"""The central model representing an art idea."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.associations import idea_collections, idea_mediums


def utc_now():
    """Return the current timezone-aware UTC time."""
    return datetime.now(timezone.utc)


class ProjectIdea(db.Model):
    """An idea that the user wants to develop into an artwork."""

    __tablename__ = "project_ideas"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    collections: Mapped[list["Collection"]] = relationship(
        secondary=idea_collections,
        back_populates="ideas",
    )
    mediums: Mapped[list["Medium"]] = relationship(
        secondary=idea_mediums,
        back_populates="ideas",
    )
    palettes: Mapped[list["ColorPalette"]] = relationship(
        back_populates="idea",
        cascade="all, delete-orphan",
    )
    reference_images: Mapped[list["ReferenceImage"]] = relationship(
        back_populates="idea",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<ProjectIdea {self.id}: {self.title!r}>"

