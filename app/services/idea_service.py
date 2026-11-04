"""Business logic for creating and managing art ideas."""

import re

from app.extensions import db
from app.models import (Collection, ColorPalette, Medium, PaletteColor, ProjectIdea,)


class IdeaService:
    """Coordinate operations involving project ideas."""

    MAX_PALETTE_COLORS = 12

    @staticmethod
    def create(title, description="", medium_ids=None, collection_ids=None):
        """Create an idea and optionally assign mediums and collections."""
        title = title.strip()

        if not title:
            raise ValueError("An idea must have a title.")

        idea = ProjectIdea(
            title=title,
            description=description.strip(),
        )

        if medium_ids:
            idea.mediums = db.session.scalars(
                db.select(Medium).where(Medium.id.in_(medium_ids))
            ).all()

        if collection_ids:
            idea.collections = db.session.scalars(
                db.select(Collection).where(
                    Collection.id.in_(collection_ids)
                )
            ).all()

        db.session.add(idea)
        db.session.commit()
        return idea

    @staticmethod
    def get_by_id(idea_id):
        """Retrieve one idea by its ID."""
        return db.session.get(ProjectIdea, idea_id)

    @staticmethod
    def list_all():
        """Return all ideas, newest first."""
        return db.session.scalars(
            db.select(ProjectIdea).order_by(
                ProjectIdea.created_at.desc(),
                ProjectIdea.id.desc(),
            )
        ).all()

    @staticmethod
    def update(
        idea_id,
        title,
        description="",
        medium_ids=None,
        collection_ids=None,
    ):
        """Update an idea and its assigned mediums and collections."""
        idea = db.session.get(ProjectIdea, idea_id)

        if idea is None:
            return None

        title = title.strip()

        if not title:
            raise ValueError("An idea must have a title.")

        idea.title = title
        idea.description = description.strip()

        if medium_ids is not None:
            idea.mediums = (
                db.session.scalars(
                    db.select(Medium).where(Medium.id.in_(medium_ids))
                ).all()
                if medium_ids
                else []
            )

        if collection_ids is not None:
            idea.collections = (
                db.session.scalars(
                    db.select(Collection).where(
                        Collection.id.in_(collection_ids)
                    )
                ).all()
                if collection_ids
                else []
            )

        db.session.commit()
        return idea

    @staticmethod
    def delete(idea_id):
        """Delete an idea and its dependent records."""
        idea = db.session.get(ProjectIdea, idea_id)

        if idea is None:
            return False

        db.session.delete(idea)
        db.session.commit()
        return True

    @staticmethod
    def _validate_palette(name, colors):
        """Validate a palette name and its hexadecimal colors."""
        name = name.strip()

        if not name:
            raise ValueError("A palette must have a name.")

        if not colors:
            raise ValueError("A palette must contain at least one color.")

        if len(colors) > IdeaService.MAX_PALETTE_COLORS:
            raise ValueError(
                f"A palette cannot contain more than "
                f"{IdeaService.MAX_PALETTE_COLORS} colors."
            )

        for color in colors:
            if not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
                raise ValueError(f"Invalid hexadecimal color: {color}")

        return name, [color.upper() for color in colors]

    @staticmethod
    def add_palette(idea_id, name, colors):
        """Create a named color palette for an idea."""
        idea = db.session.get(ProjectIdea, idea_id)

        if idea is None:
            return None

        name, colors = IdeaService._validate_palette(name, colors)

        palette = ColorPalette(name=name, idea=idea)
        palette.colors = [
            PaletteColor(hex_code=color, position=index)
            for index, color in enumerate(colors)
        ]

        db.session.add(palette)
        db.session.commit()
        return palette

    @staticmethod
    def update_palette(palette_id, name, colors):
        """Update a palette's name and its individual colors."""
        palette = db.session.get(ColorPalette, palette_id)

        if palette is None:
            return None

        name, colors = IdeaService._validate_palette(name, colors)

        palette.name = name

        # Replace the existing colors. The relationship's
        # delete-orphan cascade removes the old color records.
        palette.colors = [
            PaletteColor(hex_code=color, position=index)
            for index, color in enumerate(colors)
        ]

        db.session.commit()
        return palette