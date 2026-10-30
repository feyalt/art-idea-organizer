
"""Association tables for many-to-many relationships."""

from app.extensions import db


idea_collections = db.Table(
    "idea_collections",
    db.Column(
        "idea_id",
        db.Integer,
        db.ForeignKey("project_ideas.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "collection_id",
        db.Integer,
        db.ForeignKey("collections.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


idea_mediums = db.Table(
    "idea_mediums",
    db.Column(
        "idea_id",
        db.Integer,
        db.ForeignKey("project_ideas.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "medium_id",
        db.Integer,
        db.ForeignKey("mediums.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)