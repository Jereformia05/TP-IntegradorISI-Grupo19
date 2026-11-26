from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from myapp.extensions import db
from myapp.models.question import Question
from myapp.models.tag import Tag
from myapp.models.user import TUsuario, User
from myapp.services.agent_service import process_question_for_agent

web_bp = Blueprint("web", __name__)


def _find_user_by_email(email: str):
    user = User.query.filter_by(email=email).first()
    if user is None and TUsuario is not None:
        user = TUsuario.query.filter_by(email=email).first()
    return user


@web_bp.get("/")
@web_bp.get("/preguntas")
def list_questions():
    questions = Question.query.order_by(Question.id.desc()).all()
    return render_template("questions/index.html", questions=questions)


@web_bp.route("/preguntas/nueva", methods=["GET", "POST"])
def create_question_view():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        category_id = request.form.get("category_id")
        tags_str = request.form.get("tags", "")

        if not title or not content:
            flash("Título y contenido son requeridos", "error")
            return render_template("questions/create.html")

        user_id = session.get("user_id") or 1  # Usuario por defecto para testing
        cat_id = int(category_id) if category_id and category_id.isdigit() else None

        question = Question(
            title=title,
            content=content,
            author_id=user_id,
            category_id=cat_id,
        )

        # Procesar Tags
        if tags_str:
            tag_names = [t.strip().lstrip("#") for t in tags_str.split(",") if t.strip()]
            for name in tag_names:
                tag = Tag.query.filter_by(name=name).first()
                if not tag:
                    tag = Tag(name=name)
                    db.session.add(tag)
                question.tags.append(tag)

        db.session.add(question)
        db.session.commit()

        # Disparar agente de IA si contiene #ia-help
        process_question_for_agent(question)

        flash("Pregunta publicada con éxito", "success")
        return redirect(url_for("web.question_detail", question_id=question.id))

    return render_template("questions/create.html")


@web_bp.get("/preguntas/<int:question_id>")
def question_detail(question_id: int):
    question = Question.query.get_or_404(question_id)
    return render_template("questions/detail.html", question=question)


@web_bp.route("/login", methods=["GET", "POST"])
def login_view():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        user = _find_user_by_email(email)

        valid_password = False
        if user is not None:
            if hasattr(user, "check_password"):
                valid_password = user.check_password(password)
            elif hasattr(user, "password"):
                valid_password = user.password == password

        if user is not None and valid_password:
            session["user_id"] = user.id
            session["user_email"] = getattr(user, "email", email)
            flash("Sesión iniciada correctamente", "success")
            return redirect(url_for("web.list_questions"))

        flash("Credenciales inválidas", "error")

    return render_template("auth/login.html")


@web_bp.route("/register", methods=["GET", "POST"])
def register_view():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        if not email or not password:
            flash("Email y contraseña son requeridos", "error")
            return render_template("auth/register.html")

        if _find_user_by_email(email) is not None:
            flash("El email ya está registrado", "error")
            return render_template("auth/register.html")

        user = User(email=email)
        if hasattr(user, "set_password"):
            user.set_password(password)
        elif hasattr(user, "password"):
            user.password = password

        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        session["user_email"] = user.email
        flash("Cuenta creada con éxito", "success")
        return redirect(url_for("web.list_questions"))

    return render_template("auth/register.html")


@web_bp.get("/logout")
def logout_view():
    session.clear()
    flash("Sesión cerrada", "info")
    return redirect(url_for("web.list_questions"))