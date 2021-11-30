from . import home
from flask import redirect, url_for, render_template, jsonify
from ..models.model_user import User


@home.route("/")
def homepage():
    user = User(
        first_name="Geovane",
        last_name="Carvalho",
        email="geovane@gmail.com",
        password="asdf123",
    )

    user.save()
    return render_template("homepage.html")
