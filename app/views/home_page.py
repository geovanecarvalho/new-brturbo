from flask_login import login_manager
from . import home
from flask import redirect, url_for, render_template, jsonify, session, request
from ..models.model_user import User
from flask_login import login_required, current_user

from ..services.scraping.brturbo import Brturbo
from scrapy.crawler import CrawlerRunner
import json


import subprocess


@home.route("/")
def homepage():

    if session.get("user_name") == None:
        user_name = None
    else:
        user_name = session.get("user_name")

    if session.get("token") == None:
        token = None
    else:
        token = session.get("token")

    if session.get("game") == 0:
        game = None

    else:
        game = session.get("game")

    print(game, token, user_name)

    if user_name != None and token != None and game != None:
        session["user_name"] = None
        session["token"] = None
        session["game"] = None

    return render_template("homepage.html", user_name=user_name, token=token, game=game)


@home.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    user = User.objects(id=session["user_id"]).first()

    return render_template("dashboard/dashboard_user.html", user=user)
