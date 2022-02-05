from flask_wtf import FlaskForm
from wtforms.fields import EmailField
from wtforms.fields import PasswordField, BooleanField, SubmitField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, Length


class TokenForm(FlaskForm):
    token = StringField(validators=[DataRequired(message="Campo Obrigatório!")])
    enviar = SubmitField()
