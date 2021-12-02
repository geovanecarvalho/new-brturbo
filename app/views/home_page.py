import re
from flask_login import login_manager
from . import home
from flask import redirect, url_for, render_template, jsonify, session
from ..models.model_user import User
from flask_login import login_required, current_user


@home.route("/")
def homepage():
    user = User(
        first_name="Geovane",
        last_name="Carvalho",
        email="geovane@gmail.com",
        password="asdf123",
    )

    return render_template("homepage.html")


@home.route("/dashboard")
@login_required
def dashboard():
    user = User.objects(id=session["user_id"]).first()

    return render_template("dashboard/dashboard_user.html", user=user)
