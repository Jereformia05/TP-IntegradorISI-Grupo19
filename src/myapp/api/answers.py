from flask import Blueprint, jsonify, request
from myapp.extensions import db
from myapp.models.answer import Answer

answers_bp = Blueprint("answers", __name__)


# 1. Publicar una respuesta para una pregunta
@answers_bp.post("/api/questions/<int:question_id>/answers")
def create_answer(question_id):
    data = request.get_json() or {}
    text = data.get("text")
    user_id = data.get("user_id")
    
    if not text:
        return jsonify({"error": "El texto de la respuesta es obligatorio"}), 400
    
    answer = Answer(
        text=text,
        question_id=question_id,
        user_id=user_id,
        author_type="USER",
        is_accepted=False,
    )
    db.session.add(answer)
    db.session.commit()
    
    return (
        jsonify(
            {
                "id": answer.id,
                "text": answer.text,
                "question_id": answer.question_id,
                "user_id": answer.user_id,
                "author_type": answer.author_type,
                "is_accepted": answer.is_accepted,
            }
        ),
        201,
    )
    
# 2. Marcar una respuesta como aceptada
@answers_bp.patch("/api/answers/<int:answer_id>/accept")
def accept_answer(answer_id):
    answer = db.session.get(Answer, answer_id)
    if not answer:
        return jsonify({"error": "Respuesta no encontrada"}), 404
    
    answer.is_accepted = True
    db.session.commit()
    
    return jsonify(
        {
            "id": answer.id,
            "is_accepted": answer.is_accepted,
            "message": "Respuesta marcada como aceptada",
        }
    )