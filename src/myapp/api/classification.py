from flask import Blueprint, jsonify, request

from myapp.extensions import db
from myapp.models.category import Category
from myapp.models.question import Question
from myapp.models.tag import Tag

classification_bp = Blueprint("classification", __name__, url_prefix="/api")


# --- CATEGORÍAS ---
@classification_bp.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories]), 200


@classification_bp.route("/categories", methods=["POST"])
def create_category():
    data = request.get_json() or {}
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"error": "El nombre de la categoría es obligatorio"}), 400

    if Category.query.filter_by(name=name).first():
        return jsonify({"error": "La categoría ya existe"}), 409

    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201


# --- TAGS ---
@classification_bp.route("/tags", methods=["GET"])
def get_tags():
    tags = Tag.query.all()
    return jsonify([t.to_dict() for t in tags]), 200


@classification_bp.route("/tags", methods=["POST"])
def create_tag():
    data = request.get_json() or {}
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"error": "El nombre del tag es obligatorio"}), 400

    if Tag.query.filter_by(name=name).first():
        return jsonify({"error": "El tag ya existe"}), 409

    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return jsonify(tag.to_dict()), 201


# --- ASOCIAR TAGS A UNA PREGUNTA ---
@classification_bp.route("/questions/<int:question_id>/tags", methods=["POST", "PUT"])
def assign_tags_to_question(question_id):
    question = db.session.get(Question, question_id)
    if not question:
        return jsonify({"error": "Pregunta no encontrada"}), 404

    data = request.get_json() or {}
    tag_ids = data.get("tag_ids", [])

    if not isinstance(tag_ids, list):
        return jsonify({"error": "tag_ids debe ser una lista"}), 400

    unique_ids = set(tag_ids)
    tags = Tag.query.filter(Tag.id.in_(unique_ids)).all()

    question.tags = tags
    db.session.commit()

    return jsonify(
        {
            "question_id": question.id,
            "tags": [t.to_dict() for t in question.tags],
        }
    ), 200
