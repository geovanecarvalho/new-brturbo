import crochet

crochet.setup()
import os
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
import time
from . import scrapy
from ..services.scraping.brturbo import Brturbo
from ..models.model_user import User
from flask_login import login_user

output_data = []
crawl_runner = CrawlerRunner()


@scrapy.route("/add_game", methods=["GET", "POST"])
def add_game():
    user = User.objects(id=session["user_id"]).first()

    if len(user.gamer) > 0:
        login_user(user)
        return redirect(url_for("home.dashboard"))

    if request.method == "POST":
        s = request.form["gamer"]
        global baseURL
        baseURL = s

        if os.path.exists("warzone.json"):
            os.remove("warzone.json")

        return redirect(url_for("scrapy.scrape"))

    return render_template("auth/add_game.html")


@scrapy.route("/scrape")
def scrape():

    scrape_with_crochet(baseURL=baseURL)

    time.sleep(20)

    user = User.objects(id=session["user_id"]).first()

    user.gamer = output_data

    user.save()

    jsonify(output_data)

    return redirect(url_for("home.dashboard"))


@crochet.run_in_reactor
def scrape_with_crochet(baseURL):

    dispatcher.connect(_crawler_result, signal=signals.item_scraped)

    eventual = crawl_runner.crawl(Brturbo, category=baseURL)
    return eventual


def _crawler_result(item, response, spider):
    if len(output_data) > 0:
        output_data.pop()
    else:
        output_data.append(dict(item))


# @app.route('/')
# def index():
#     dados = crawl_runner.crawl(Brturbo)
