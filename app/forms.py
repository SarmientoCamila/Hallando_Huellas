# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TelField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegisterUserForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired()])
    surname = StringField("Apellido", validators=[DataRequired()])
    address = StringField("Domicilio", validators=[DataRequired()])
    phone = TelField("Teléfono", validators=[DataRequired(), Length(min=7, max=15)])
    email = EmailField("Correo electrónico", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired(), EqualTo("confirm_password"), Length(min=8, max=20)])
    confirm_password = PasswordField("Confirmar contraseña", validators=[DataRequired()])
    submit = SubmitField("Registrarse")

class LoginForm(FlaskForm):
    email = EmailField("Correo electrónico", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar sesión")
