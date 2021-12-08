from logging import exception
from flask_login.utils import login_required
from . import auth
from flask import render_template, request, session, redirect, url_for, jsonify, flash
from ..models.model_user import User
from flask_login import LoginManager, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions.extension import login_manager
from ..services.token.token_generate import Token
from secrets import token_hex
from datetime import datetime

token_key = Token()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("home.homepage"))


@login_manager.user_loader
def current_user(user_id):
    user = User.objects(id=user_id).first()
    if user is None:
        return user

    elif len(user.gamer) > 0:
        return user


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.objects(email=email).first()

        if not user:

            return redirect(url_for("auth.login"))

        if not check_password_hash(user.password, password):

            return redirect(url_for("auth.login"))

        if user:
            token_key.generate_new_token()
            session["user_id"] = str(user.id)
            return redirect(url_for("auth.token"))

    return render_template("auth/login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User()
        user.first_name = request.form["first_name"]
        user.last_name = request.form["last_name"]
        user.email = request.form["email"]
        user.password = generate_password_hash(request.form["password"])

        user.save()

        session["user_id"] = str(user.id)
        token_key.generate_new_token()

        return redirect(url_for("auth.token"))
    return render_template("auth/register.html")


@auth.route("/token", methods=["GET", "POST"])
def token():

    token = token_key.get_token()
    print(token)
    if request.method == "POST":

        if request.form["token"] == token:
            user_id = session["user_id"]
            user = User.objects(id=user_id).first()

            return redirect(url_for("scrapy.add_game"))
    return render_template("auth/token.html")


@auth.route("/recover/email/password", methods=["GET", "POST"])
def recover_password():
    form = False
    if request.method == "POST":
        email = request.form["email"]
        user = User.objects(email=email).first()

        if user is None:
            flash("Email não encontrado ferifique se este email esta correto")

        flash("Verifique o sua caixa de email para redefinir a senha")
        print(f"http://localhost:5000/new_password/{user.id}")

    return render_template("auth/recover.html", form=form)


@auth.route("/new_password/<id>", methods=["GET", "POST"])
def teste(id):

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

            flash("As senhas são difentes")
        except:
            return redirect(url_for("auth.recover_password"))

    return render_template("auth/new_password.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    session["user_id"] = None
    return redirect(url_for("home.homepage"))
