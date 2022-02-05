from typing import Pattern
from flask_wtf import FlaskForm
from wtforms.fields import EmailField
from wtforms.fields import PasswordField, BooleanField, SubmitField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, Length


class AddGamerForm(FlaskForm):
    url = StringField(
        validators=[DataRequired(pattern="https://cod.tracker.gg/warzone/profile/(.*)")]
    )
    save_game = SubmitField("Salvar Jogo")
