from ..extensions.mongodbConfig import db
from datetime import datetime
from flask_login import UserMixin


class User(UserMixin, db.Document):
    first_name = db.StringField(required=True, max_length=50)
    last_name = db.StringField(required=True, max_length=50)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    gamer = db.ListField()
    token = db.StringField()
    update_at = db.DateTimeField(requered=True, default=datetime.now)
    create_at = db.DateTimeField(requered=True, default=datetime.now)
