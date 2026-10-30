
"""Routes for creating and managing art ideas."""

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.models import Collection, Medium
from app.services.idea_service import IdeaService


ideas_bp = Blueprint("ideas", __name__, url_prefix="/ideas")


@ideas_bp.route("/new", methods=["GET", "POST"])
def create_idea():
    """Display the creation form and process new ideas."""
    if request.method == "POST":
        try:
            idea = IdeaService.create(
                title=request.form.get("title", ""),
                description=request.form.get("description", ""),
                medium_ids=request.form.getlist("medium_ids", type=int),
                collection_ids=request.form.getlist("collection_ids", type=int),
            )
        except ValueError as error:
            flash(str(error), "error")
        else:
            flash("Your idea has been saved.", "success")
            return redirect(url_for("ideas.idea_detail", idea_id=idea.id))

    return render_template(
        "idea_form.html",
        idea=None,
        mediums=Medium.query.order_by(Medium.name).all(),
        collections=Collection.query.order_by(Collection.name).all(),
    )


@ideas_bp.get("/<int:idea_id>")
def idea_detail(idea_id):
    """Display one idea."""
    idea = IdeaService.get_by_id(idea_id)

    if idea is None:
        abort(404)

    return render_template("idea_detail.html", idea=idea)


@ideas_bp.route("/<int:idea_id>/edit", methods=["GET", "POST"])
def edit_idea(idea_id):
    """Display the editing form and save changes."""
    idea = IdeaService.get_by_id(idea_id)

    if idea is None:
        abort(404)

    if request.method == "POST":
        try:
            updated_idea = IdeaService.update(
                idea_id=idea_id,
                title=request.form.get("title", ""),
                description=request.form.get("description", ""),
                medium_ids=request.form.getlist("medium_ids", type=int),
                collection_ids=request.form.getlist("collection_ids", type=int),
            )
        except ValueError as error:
            flash(str(error), "error")
        else:
            flash("Your changes have been saved.", "success")
            return redirect(
                url_for("ideas.idea_detail", idea_id=updated_idea.id)
            )

    return render_template(
        "idea_form.html",
        idea=idea,
        mediums=Medium.query.order_by(Medium.name).all(),
        collections=Collection.query.order_by(Collection.name).all(),
    )


@ideas_bp.post("/<int:idea_id>/delete")
def delete_idea(idea_id):
    """Delete an idea after a form submission."""
    if not IdeaService.delete(idea_id):
        abort(404)

    flash("Idea deleted.", "success")
    return redirect(url_for("main.index"))
