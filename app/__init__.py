from dynaconf.base import Settings
from flask import Flask
import flask_mongoengine
from .extensions import extension
from .extensions import mongodbConfig
from .views import home as home_blueprint
from .views import auth as auth_blueprint


def create_app():
    app = Flask(__name__)
    extension.init_app(app)

    mongodbConfig.init_app(app)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(auth_blueprint)

    return app
