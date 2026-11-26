from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from myapp.extensions import db
from myapp.models.answer import Answer
from myapp.models.question import Question
from myapp.models.tag import Tag
from myapp.models.user import User
from myapp.services.agent_service import process_question_for_agent

web_bp = Blueprint("web", __name__)


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
            text=content,
            user_id=session.get("user_id"),
            category_id=category_id if category_id else None,
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


@web_bp.post("/preguntas/<int:question_id>/respuestas")
def add_answer_view(question_id: int):
    question = Question.query.get_or_404(question_id)
    text = (request.form.get("text") or request.form.get("content") or "").strip()

    if not text:
        flash("El texto de la respuesta es obligatorio.", "error")
        return redirect(url_for("web.question_detail", question_id=question.id))

    user_id = session.get("user_id") or 1

    answer = Answer(
        text=text,
        question_id=question.id,
        user_id=user_id,
        author_type="USER",
        is_accepted=False,
    )
    db.session.add(answer)
    db.session.commit()

    flash("Respuesta publicada con éxito.", "success")
    return redirect(url_for("web.question_detail", question_id=question.id))


@web_bp.post("/preguntas/<int:question_id>/respuestas/<int:answer_id>/aceptar")
def accept_answer_view(question_id: int, answer_id: int):
    question = Question.query.get_or_404(question_id)
    answer = Answer.query.filter_by(id=answer_id, question_id=question.id).first_or_404()

    for other in question.answers:
        other.is_accepted = False
    answer.is_accepted = True
    db.session.commit()

    flash("Respuesta marcada como aceptada.", "success")
    return redirect(url_for("web.question_detail", question_id=question.id))


@web_bp.route("/login", methods=["GET", "POST"])
def login_view():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        usuario = User.query.filter_by(email=email).first()
        if not usuario or not usuario.check_password(password):
            flash("Correo o contraseña incorrectos.", "error")
            return redirect(url_for("web.login_view"))

        session["user_id"] = usuario.id
        session["user_email"] = usuario.email
        flash("¡Sesión iniciada con éxito!", "success")
        return redirect(url_for("web.list_questions"))

    return render_template("auth/login.html")


@web_bp.route("/register", methods=["GET", "POST"])
def register_view():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        if not email or not password:
            flash("Email y contraseña son requeridos", "error")
            return render_template("auth/register.html")

        if User.query.filter_by(email=email).first():
            flash("El correo electrónico ya está registrado.", "error")
            return redirect(url_for("web.register_view"))

        nuevo_usuario = User(email=email)
        nuevo_usuario.set_password(password)

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("¡Cuenta creada exitosamente! Por favor iniciá sesión.", "success")
        return redirect(url_for("web.login_view"))

    return render_template("auth/register.html")


@web_bp.get("/logout")
def logout_view():
    session.clear()
    flash("Sesión cerrada", "info")
    return redirect(url_for("web.list_questions"))