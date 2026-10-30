
"""Routes for managing collections of art ideas."""

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.services.collection_service import CollectionService


collections_bp = Blueprint("collections", __name__, url_prefix="/collections")


@collections_bp.get("/")
def index():
    """Display all collections."""
    collections = CollectionService.list_all()
    return render_template("collections.html", collections=collections)


@collections_bp.post("/new")
def create():
    """Create a collection."""
    name = request.form.get("name", "")
    description = request.form.get("description", "")

    try:
        CollectionService.create(name, description)
    except ValueError as error:
        flash(str(error), "error")
    else:
        flash("Collection created.", "success")

    return redirect(url_for("collections.index"))


@collections_bp.post("/<int:collection_id>/delete")
def delete(collection_id):
    """Delete a collection without deleting its ideas."""
    if not CollectionService.delete(collection_id):
        abort(404)

    flash("Collection deleted.", "success")
    return redirect(url_for("collections.index"))
