
"""External visual references attached to art ideas."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class ReferenceImage(db.Model):
    """A URL pointing to an image that inspires an art idea."""

    __tablename__ = "reference_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    caption: Mapped[str] = mapped_column(
        String(255),
        default="",
        nullable=False,
    )
    position: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    idea_id: Mapped[int] = mapped_column(
        ForeignKey("project_ideas.id", ondelete="CASCADE"),
        nullable=False,
    )

    idea: Mapped["ProjectIdea"] = relationship(
        back_populates="reference_images",
    )

    def __repr__(self) -> str:
        return f"<ReferenceImage {self.id}: {self.url!r}>"
