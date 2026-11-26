from datetime import datetime

from myapp.extensions import db
from myapp.models.tag import question_tags


class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)

    tags = db.relationship(
        "Tag",
        secondary=question_tags,
        back_populates="questions",
        lazy="subquery",
    )
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    category_id = db.Column(db.Integer, nullable=False)
