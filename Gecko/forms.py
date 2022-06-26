from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, EqualTo, Email, DataRequired, ValidationError
from Gecko.models import Usuario

class RegisterForm(FlaskForm):
    nombre = StringField(label="Nombre*", validators=[Length(min=3, max=50, message="El nombre debe tener como minimo 3 letras."), DataRequired(message="Debe ingresar un nombre para poder registrarse.")]) 
    username = StringField(label="Username")
    email = StringField(label="Correo Electronico*", validators=[Email(message="Correo electronico invalido."), DataRequired()])
    password = PasswordField(label="Contraseña*", validators=[Length(min=8, message="La contraseña debe tener como minimo 8 caracteres."), DataRequired()])
    password_confirmation = PasswordField(label="Repetir Contraseña*", validators=[EqualTo("password", message="Las contraseñas deben ser iguales."), DataRequired()])
    acepto_terminos = BooleanField(label="Acepto", validators=[DataRequired(message="Debe aceptar los terminos & condiciones.")])
    submit = SubmitField(label="Crear")

class LoginForm(FlaskForm):
    email = StringField(label="Correo Electronico*", validators=[DataRequired()])
    password = PasswordField(label="Contraseña*", validators=[DataRequired(message="Debe Ingresar una Contraseña.")])
    remember_me = BooleanField(label="Recordarme")
    submit = SubmitField(label="Ingresar")

class UrlForm(FlaskForm):
    game = StringField(label="Game Name*", validators=[DataRequired()])
    url = StringField(label="Game Url*", validators=[DataRequired()])
    submit = SubmitField(label="Search")