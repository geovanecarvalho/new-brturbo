from flask import Blueprint

home = Blueprint("home", __name__)

auth = Blueprint("auth", __name__)

scrapy = Blueprint("scrapy", __name__)

from . import home_page, auth_user, scrapy_game
