def test_create_answer(client):
    """Verifica la creación de una respuesta para una pregunta."""
    response = client.post(
        "/api/questions/1/answers",
        json={"text": "Esta es una respuesta de prueba", "user_id": 1},
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["text"] == "Esta es una respuesta de prueba"
    assert data["question_id"] == 1
    assert data["is_accepted"] is False


def test_accept_answer(client):
    """Verifica que se pueda marcar una respuesta como aceptada."""
    # 1. Crear una respuesta de prueba
    res_create = client.post(
        "/api/questions/1/answers",
        json={"text": "Respuesta para aceptar", "user_id": 1},
    )

    answer_id = res_create.get_json()["id"]

    # 2. Aceptar la respuesta creada
    response = client.patch(f"/api/answers/{answer_id}/accept")
    assert response.status_code == 200
    assert response.get_json()["is_accepted"] is True
