from logging import exception
from flask_login.utils import login_required

from app.forms.form_login import LoginForm
from app.forms.form_register import RegisterForm
from app.forms.form_token import TokenForm
from . import auth
from flask import render_template, request, session, redirect, url_for, jsonify, flash
from ..models.model_user import User
from flask_login import LoginManager, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions.extension import login_manager
from ..services.token.token_generate import Token
from secrets import token_hex
from datetime import datetime
from ..services.email.email import email_new_password, email_token, enviar_email

token_key = Token()
validate_token = 0


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("home.homepage"))


@login_manager.user_loader
def current_user(user_id):
    user = User.objects(id=user_id).first()
    if user is None:
        return user

    elif len(user.gamer) > 0 and user.token == token_key.get_token():

        return user


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remenber_me = form.remenber_me.data
        user = User.objects(email=email).first()

        if not user:
            flash(message="Email não encontrado", category="danger")
            return redirect(url_for("auth.login"))

        if not check_password_hash(user.password, password):
            flash(message="Senha invalida", category="danger")
            return redirect(url_for("auth.login"))

        if user:
            token_key.generate_new_token()
            session["user_id"] = str(user.id)
            session["user_name"] = str(user.first_name)
            session["game"] = str(len(user.gamer))

            email = email_token(token_key.get_token())
            enviar_email(str(user.email), "Token de Acesso", email)

            return redirect(url_for("auth.token"))

    return render_template("auth/login.html", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data == form.password2.data:
            user = User()
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            user.password = generate_password_hash(form.password.data)

            user.save()

            session["user_id"] = str(user.id)
            session["user_name"] = str(user.first_name)
            session["game"] = str(len(user.gamer))

            token_key.generate_new_token()

            email = email_token(token_key.get_token())
            enviar_email(str(user.email), "Token de Acesso", email)

            return redirect(url_for("auth.token"))
        flash("As senhas são diferentes")
    return render_template("auth/register.html", form=form)


@auth.route("/token", methods=["GET", "POST"])
def token():
    user_id = session["user_id"]
    user = User.objects(id=user_id).first()
    token = token_key.get_token()

    form = TokenForm()

    if form.validate_on_submit():
        print(token, form.token.data)
        if form.token.data == token:
            session["token"] = token

            user.update(token=token)

            return redirect(url_for("scrapy.add_game"))

        flash(message="Token invalido!", category="danger")
    if session["user_id"] is None:
        return redirect(url_for("home.homepage"))

    return render_template("auth/token.html", form=form)


@auth.route("/token_resend")
def token_resend():
    flash(
        message="Eviamos o email com token novamente, verifique sua caixa de email ou sua caixa de span e ensira o token aqui, obrigado.",
        category="info",
    )
    user_id = session["user_id"]
    user = User.objects(id=user_id).first()

    email = email_token(token_key.get_token())
    enviar_email(str(user.email), "Token de Acesso", email)

    return redirect(url_for("auth.token"))


@auth.route("/recover/email/password", methods=["GET", "POST"])
def recover_password():
    form = False
    if request.method == "POST":

        email = request.form["email"]
        user = User.objects(email=email).first()

        if user is not None:
            flash(
                message="Enviamos um email com link para redefinição de senha.",
                category="success",
            )
            url = f"http://localhost:5000/new_password/{user.id}"
            email = render_template("email/email_redefinir_senha.html", url=url)

            enviar_email(str(user.email), "Token de Acesso", email)
        else:
            flash(
                message="Não existe este email cadastrado em nosso sistema!",
                category="danger",
            )

    return render_template("auth/recover.html", form=form)


@auth.route("/new_password/<id>", methods=["GET", "POST"])
def new_password(id):

    if request.method == "POST":
        try:
            user = User.objects(id=id).first()
            password = request.form["password"]
            password2 = request.form["password2"]
            if password == password2:
                pwd = generate_password_hash(password)
                user.update(password=pwd)
                user.update(update_at=datetime.now)

                return redirect(url_for("auth.login"))

            flash(message="As senhas não são iguais!", category="danger")
        except:
            return redirect(url_for("auth.recover_password"))

    return render_template("auth/new_password.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    session["user_id"] = None
    session["user_name"] = None
    session["game"] = None
    session["token"] = None

    return redirect(url_for("home.homepage"))
