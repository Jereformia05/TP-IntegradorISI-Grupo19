from myapp.extensions import db

question_tags = db.Table(
    "question_tags",
    db.Column(
        "question_id", db.Integer, db.ForeignKey("questions.id"), primary_key=True
    ),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    questions = db.relationship(
        "Question",
        secondary=question_tags,
        back_populates="tags",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
