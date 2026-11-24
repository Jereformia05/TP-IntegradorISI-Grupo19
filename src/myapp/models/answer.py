from datetime import datetime

from myapp.extensions import db


class Answer(db.Model):
    __tablename__ = "answers"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_accepted = db.Column(db.Boolean, default=False, nullable=False)
    # Claves foráneas (relación con las tablas de preguntas y usuarios)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    author_type = db.Column(db.String(20), default="USER", nullable=False)
    # 'USER' o 'AGENT'
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    # Opcional si la genera la IA
    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
            "is_accepted": self.is_accepted,
            "question_id": self.question_id,
            "author_type": self.author_type,
            "user_id": self.user_id,
        }
