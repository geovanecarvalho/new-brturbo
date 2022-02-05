from flask_wtf import FlaskForm
from wtforms.fields import EmailField
from wtforms.fields import PasswordField, BooleanField, SubmitField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    first_name = StringField("Seu Nome", validators=[DataRequired()])
    last_name = StringField("Seu Sobrenome", validators=[DataRequired()])
    email = EmailField("Seu Email", validators=[DataRequired()])
    password = PasswordField(
        "Sua Senha",
        validators=[
            DataRequired(),
            Length(min=6, message="O mínimo são 6 caracteres para uma senha segura."),
        ],
    )
    password2 = PasswordField(
        "Repita Sua Senha",
        validators=[
            DataRequired(),
            Length(min=6, message="O mínimo são 6 caracteres para uma senha segura."),
        ],
    )
    terms = BooleanField(
        "Eu concordo com os termos e condições", validators=[DataRequired()]
    )
    cadastrar = SubmitField("Cadastrar")
