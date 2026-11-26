def test_create_question(client):
    """Verifica la creación de una pregunta válida."""
    response = client.post(
        "/api/questions",
        json={
            "title": "¿Cómo funciona SQLAlchemy?",
            "text": "Tengo dudas sobre relaciones y migraciones.",
            "category_id": 1,
            "user_id": 1,
        },
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "¿Cómo funciona SQLAlchemy?"
    assert data["text"] == "Tengo dudas sobre relaciones y migraciones."
    assert data["category_id"] == 1
    assert data["user_id"] == 1
    assert data["id"] is not None


def test_create_question_without_category_fails(client):
    """Verifica que se rechace una pregunta si falta la categoría obligatoria."""
    response = client.post(
        "/api/questions",
        json={
            "title": "Pregunta sin categoría",
            "text": "Falta el campo category_id",
            "user_id": 1,
        },
    )

    assert response.status_code == 400


def test_list_and_get_question(client):
    """Verifica el listado y la consulta de una pregunta por ID."""
    created = client.post(
        "/api/questions",
        json={
            "title": "Detalle de prueba",
            "text": "Cuerpo de prueba",
            "category_id": 2,
        },
    ).get_json()
    question_id = created["id"]

    list_res = client.get("/api/questions")
    assert list_res.status_code == 200
    assert any(q["id"] == question_id for q in list_res.get_json())

    detail_res = client.get(f"/api/questions/{question_id}")
    assert detail_res.status_code == 200
    assert detail_res.get_json()["title"] == "Detalle de prueba"
