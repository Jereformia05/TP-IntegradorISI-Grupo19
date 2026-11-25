from flask import Blueprint, jsonify, request
from myapp.extensions import db
from myapp.models.question import Question

questions_bp = Blueprint("questions", __name__)


def _serialize_question(question):
    return {
        "id": question.id,
        "title": question.title,
        "text": question.text,
        "created_at": question.created_at.isoformat() if question.created_at else None,
        "user_id": question.user_id,
        "category_id": question.category_id,
    }


@questions_bp.get("/api/questions")
def list_questions():
    questions = db.session.scalars(db.select(Question)).all()
    return jsonify([_serialize_question(q) for q in questions]), 200


@questions_bp.post("/api/questions")
def create_question():
    data = request.get_json() or {}
    title = data.get("title")
    text = data.get("text")
    category_id = data.get("category_id")
    user_id = data.get("user_id")

    if not title:
        return jsonify({"error": "El título de la pregunta es obligatorio"}), 400
    if not text:
        return jsonify({"error": "El cuerpo de la pregunta es obligatorio"}), 400
    if category_id is None or category_id == "":
        return jsonify({"error": "La categoría es obligatoria"}), 400

    question = Question(
        title=title,
        text=text,
        category_id=category_id,
        user_id=user_id,
    )
    db.session.add(question)
    db.session.commit()

    return jsonify(_serialize_question(question)), 201


@questions_bp.get("/api/questions/<int:question_id>")
def get_question(question_id):
    question = db.session.get(Question, question_id)
    if not question:
        return jsonify({"error": "Pregunta no encontrada"}), 404

    return jsonify(_serialize_question(question)), 200