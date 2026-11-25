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