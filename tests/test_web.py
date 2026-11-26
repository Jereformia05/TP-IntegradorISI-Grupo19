def test_web_index_route(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Preguntas de la Comunidad" in res.data


def test_web_login_page(client):
    res = client.get("/login")
    assert res.status_code == 200
    assert b"Iniciar Sesion" in res.data or b"Iniciar" in res.data