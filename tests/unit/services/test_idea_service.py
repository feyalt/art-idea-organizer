
"""Tests for IdeaService."""

import pytest

from app.models import ProjectIdea
from app.services.idea_service import IdeaService


def test_create_idea(app):
    idea = IdeaService.create(
        title="Moonlit Garden",
        description="Flowers under moonlight.",
    )

    assert idea.id is not None
    assert idea.title == "Moonlit Garden"
    assert idea.description == "Flowers under moonlight."


def test_create_idea_trims_title(app):
    idea = IdeaService.create("  Botanical Study  ")

    assert idea.title == "Botanical Study"


def test_create_idea_rejects_empty_title(app):
    with pytest.raises(ValueError, match="title"):
        IdeaService.create("   ")


def test_update_idea(app):
    idea = IdeaService.create("Initial Idea")

    updated = IdeaService.update(
        idea.id,
        title="Revised Idea",
        description="A new direction.",
    )

    assert updated.title == "Revised Idea"
    assert updated.description == "A new direction."


def test_update_missing_idea_returns_none(app):
    assert IdeaService.update(999, title="Missing") is None


def test_delete_idea(app):
    idea = IdeaService.create("Temporary Idea")

    assert IdeaService.delete(idea.id) is True
    assert IdeaService.get_by_id(idea.id) is None


def test_list_all_ideas(app):
    IdeaService.create("First Idea")
    IdeaService.create("Second Idea")

    ideas = IdeaService.list_all()

    assert len(ideas) == 2
    assert {idea.title for idea in ideas} == {
        "First Idea",
        "Second Idea",
    }
