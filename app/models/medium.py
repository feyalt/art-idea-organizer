
"""Art mediums that can be assigned to ideas."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.associations import idea_mediums


class Medium(db.Model):
    """A reusable art medium, such as watercolor or charcoal."""

    __tablename__ = "mediums"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(80),
        unique=True,
        nullable=False,
    )

    ideas: Mapped[list["ProjectIdea"]] = relationship(
        secondary=idea_mediums,
        back_populates="mediums",
    )

    def __repr__(self) -> str:
        return f"<Medium {self.id}: {self.name!r}>"
