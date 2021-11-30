from flask_login import LoginManager, UserMixin
from ..extensions.mongodbConfig import db
from datetime import datetime


class User(db.Document):
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    email = db.EmailField(required=True)
    password = db.StringField(max_length=50)
    create_at = db.DateTimeField(default=datetime.now)
