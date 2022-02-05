from flask_wtf import FlaskForm
from wtforms.fields import EmailField
from wtforms.fields import PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    email = EmailField(
        "Email", validators=[DataRequired(message="O campo de Email é obrigatório.")]
    )
    password = PasswordField(
        "Senha",
        validators=[
            DataRequired(),
            Length(min=6, message="O campo deve conter entre 6 á 8 caracteres"),
        ],
    )
    remenber_me = BooleanField("Lembra-me")
    submit = SubmitField("Logar")
