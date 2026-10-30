
"""Collections used to organize art ideas."""

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.associations import idea_collections


class Collection(db.Model):
    """A user-created group of art ideas."""

    __tablename__ = "collections"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    ideas: Mapped[list["ProjectIdea"]] = relationship(
        secondary=idea_collections,
        back_populates="collections",
    )

    def __repr__(self) -> str:
        return f"<Collection {self.id}: {self.name!r}>"

