
"""Search and filter art ideas."""

from sqlalchemy import or_, select

from app.extensions import db
from app.models import (
    Collection,
    ColorPalette,
    Medium,
    PaletteColor,
    ProjectIdea,
)


class SearchService:
    """Find ideas using text queries and optional filters."""

    @staticmethod
    def search(
        query=None,
        medium_id=None,
        collection_id=None,
        color=None,
    ):
        """Search ideas using any combination of supported criteria."""
        statement = select(ProjectIdea)

        if query and query.strip():
            term = f"%{query.strip()}%"

            text_match = or_(
                ProjectIdea.title.ilike(term),
                ProjectIdea.description.ilike(term),
                ProjectIdea.mediums.any(Medium.name.ilike(term)),
                ProjectIdea.collections.any(Collection.name.ilike(term)),
                ProjectIdea.palettes.any(
                    ColorPalette.colors.any(PaletteColor.hex_code.ilike(term))
                ),
            )

            statement = statement.where(text_match)

        if medium_id is not None:
            statement = statement.where(
                ProjectIdea.mediums.any(Medium.id == medium_id)
            )

        if collection_id is not None:
            statement = statement.where(
                ProjectIdea.collections.any(
                    Collection.id == collection_id
                )
            )

        if color and color.strip():
            color_term = f"%{color.strip()}%"

            statement = statement.where(
                ProjectIdea.palettes.any(
                    ColorPalette.colors.any(
                        PaletteColor.hex_code.ilike(color_term)
                    )
                )
            )

        statement = statement.order_by(
            ProjectIdea.created_at.desc(),
            ProjectIdea.id.desc(),
        )

        return db.session.scalars(statement).all()
