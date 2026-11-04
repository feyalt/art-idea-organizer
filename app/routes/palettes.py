"""Routes for managing color palettes."""

from flask import Blueprint, abort, flash, redirect, request, url_for

from app.extensions import db
from app.models import ColorPalette, ProjectIdea
from app.services.idea_service import IdeaService


palettes_bp = Blueprint("palettes", __name__)


@palettes_bp.post("/ideas/<int:idea_id>/palettes")
def create_palette(idea_id):
    """Create a palette for an existing idea."""
    if db.session.get(ProjectIdea, idea_id) is None:
        abort(404)

    name = request.form.get("palette_name", "")
    colors = request.form.getlist("colors")

    try:
        IdeaService.add_palette(idea_id, name, colors)
    except ValueError as error:
        flash(str(error), "error")
    else:
        flash("Color palette saved.", "success")

    return redirect(url_for("ideas.idea_detail", idea_id=idea_id))


@palettes_bp.post("/palettes/<int:palette_id>/edit")
def edit_palette(palette_id):
    """Update a palette's name and colors."""
    palette = db.session.get(ColorPalette, palette_id)

    if palette is None:
        abort(404)

    idea_id = palette.idea_id
    name = request.form.get("palette_name", "")
    colors = request.form.getlist("colors")

    try:
        IdeaService.update_palette(palette_id, name, colors)
    except ValueError as error:
        flash(str(error), "error")
    else:
        flash("Color palette updated.", "success")

    return redirect(url_for("ideas.idea_detail", idea_id=idea_id))


@palettes_bp.post("/palettes/<int:palette_id>/delete")
def delete_palette(palette_id):
    """Delete a palette."""
    palette = db.session.get(ColorPalette, palette_id)

    if palette is None:
        abort(404)

    idea_id = palette.idea_id

    db.session.delete(palette)
    db.session.commit()

    flash("Color palette deleted.", "success")
    return redirect(url_for("ideas.idea_detail", idea_id=idea_id))