
"""Tests for CollectionService."""

import pytest

from app.models import ProjectIdea
from app.services.collection_service import CollectionService


def test_create_collection(app):
    collection = CollectionService.create(
        "Sketchbook",
        "Ideas for drawing practice.",
    )

    assert collection.id is not None
    assert collection.name == "Sketchbook"


def test_create_collection_rejects_empty_name(app):
    with pytest.raises(ValueError, match="name"):
        CollectionService.create("  ")


def test_create_collection_rejects_duplicate_name(app):
    CollectionService.create("Sketchbook")

    with pytest.raises(ValueError, match="already exists"):
        CollectionService.create("Sketchbook")


def test_add_and_remove_idea(app):
    collection = CollectionService.create("Nature")
    idea = ProjectIdea(title="Forest Study")

    from app.extensions import db
    db.session.add(idea)
    db.session.commit()

    assert CollectionService.add_idea(collection.id, idea.id) is True
    assert idea in collection.ideas

    assert CollectionService.remove_idea(collection.id, idea.id) is True
    assert idea not in collection.ideas


def test_deleting_collection_preserves_ideas(app):
    collection = CollectionService.create("Favorites")
    idea = ProjectIdea(title="Favorite Concept")

    from app.extensions import db
    db.session.add(idea)
    db.session.commit()

    CollectionService.add_idea(collection.id, idea.id)

    assert CollectionService.delete(collection.id) is True
    assert db.session.get(ProjectIdea, idea.id) is not None


def test_adding_missing_records_returns_false(app):
    assert CollectionService.add_idea(999, 999) is False
