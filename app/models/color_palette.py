
"""Color palettes and their individual colors."""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class ColorPalette(db.Model):
    """A named color palette belonging to an art idea."""

    __tablename__ = "color_palettes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    idea_id: Mapped[int] = mapped_column(
        ForeignKey("project_ideas.id", ondelete="CASCADE"),
        nullable=False,
    )

    idea: Mapped["ProjectIdea"] = relationship(back_populates="palettes")
    colors: Mapped[list["PaletteColor"]] = relationship(
        back_populates="palette",
        cascade="all, delete-orphan",
        order_by="PaletteColor.position",
    )

    def __repr__(self) -> str:
        return f"<ColorPalette {self.id}: {self.name!r}>"


class PaletteColor(db.Model):
    """A single color within a palette."""

    __tablename__ = "palette_colors"

    id: Mapped[int] = mapped_column(primary_key=True)
    hex_code: Mapped[str] = mapped_column(String(7), nullable=False)
    position: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    palette_id: Mapped[int] = mapped_column(
        ForeignKey("color_palettes.id", ondelete="CASCADE"),
        nullable=False,
    )

    palette: Mapped["ColorPalette"] = relationship(
        back_populates="colors",
    )

    def __repr__(self) -> str:
        return f"<PaletteColor {self.hex_code}>"
