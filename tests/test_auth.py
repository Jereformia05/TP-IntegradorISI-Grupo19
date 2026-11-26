def test_register_and_login(client):
    # 1\. Registro exitoso
    res_reg = client.post(
        "/api/auth/register",
        json={
            "email": "jere@utn.edu.ar",
            "password": "claveSegura123",
            "role": "USUARIO_GENERAL",
        },
    )
    assert res_reg.status_code == 201

    # 2\. Login correcto
    res_login = client.post(
        "/api/auth/login",
        json={"email": "jere@utn.edu.ar", "password": "claveSegura123"},
    )
    assert res_login.status_code == 200
    assert res_login.json["user"]["email"] == "jere@utn.edu.ar"

    # 3\. Login fallido por contraseña incorrecta
    res_fail = client.post(
        "/api/auth/login",
        json={"email": "jere@utn.edu.ar", "password": "claveIncorrecta"},
    )
    assert res_fail.status_code == 401
