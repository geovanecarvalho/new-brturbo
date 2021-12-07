from flask_login.utils import login_required
from . import auth
from flask import render_template, request, session, redirect, url_for, jsonify
from ..models.model_user import User
from flask_login import LoginManager, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions.extension import login_manager
from ..services.token.token_generate import Token

token_key = Token()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("home.homepage"))


@login_manager.user_loader
def current_user(user_id):

    return User.objects(id=user_id).first()


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
            login_user(user)
            return redirect(url_for("scrapy.add_game"))
    return render_template("auth/token.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    session["user_id"] = None
    return redirect(url_for("home.homepage"))
