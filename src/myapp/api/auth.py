from flask import Blueprint, jsonify, request

from myapp.extensions import db
from myapp.models.user import TUsuario, User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    role_str = data.get("role", "USUARIO_GENERAL")

    if not email or not password:
        return jsonify({"error": "Email y contraseña requeridos"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "El correo electrónico ya está registrado"}), 400

    role = TUsuario.ADMIN if role_str.upper() == "ADMIN" else TUsuario.USUARIO_GENERAL
    user = User(email=email, role=role)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado exitosamente", "id": user.id}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    # Valida credenciales comprobando el hash (equivale a VerificarUsuario.java)
    if not user or not user.check_password(password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    return jsonify(
        {
            "message": "Autenticación exitosa",
            "user": {"id": user.id, "email": user.email, "role": user.role.value},
        }
    ), 200
