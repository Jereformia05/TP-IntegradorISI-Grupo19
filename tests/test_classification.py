from myapp.extensions import db
from myapp.models.question import Question
from myapp.models.tag import Tag


def test_create_and_get_categories(client):
    res_post = client.post("/api/categories", json={"name": "Matemática Discreta"})
    assert res_post.status_code == 201
    assert res_post.get_json()["name"] == "Matemática Discreta"

    res_get = client.get("/api/categories")
    assert res_get.status_code == 200
    assert len(res_get.get_json()) == 1
    assert res_get.get_json()[0]["name"] == "Matemática Discreta"


def test_create_and_get_tags(client):
    res_post = client.post("/api/tags", json={"name": "python"})
    assert res_post.status_code == 201
    assert res_post.get_json()["name"] == "python"

    res_get = client.get("/api/tags")
    assert res_get.status_code == 200
    assert len(res_get.get_json()) == 1
    assert res_get.get_json()[0]["name"] == "python"


def test_question_multiple_tags_without_duplicates(client, app):
    with app.app_context():
        t1 = Tag(name="flask")
        t2 = Tag(name="sqlalchemy")
        question = Question()
        db.session.add_all([t1, t2, question])
        db.session.commit()
        q_id, t1_id, t2_id = question.id, t1.id, t2.id

    # Enviamos IDs repetidos a propósito para verificar que no se dupliquen
    res = client.post(
        f"/api/questions/{q_id}/tags",
        json={"tag_ids": [t1_id, t2_id, t1_id, t2_id]},
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["question_id"] == q_id
    assert len(data["tags"]) == 2
    assert {t["name"] for t in data["tags"]} == {"flask", "sqlalchemy"}