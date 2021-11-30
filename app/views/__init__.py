from flask import Blueprint

home = Blueprint("home", __name__)

auth = Blueprint("auth", __name__)

from . import home_page, auth_user
