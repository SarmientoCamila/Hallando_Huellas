from flask import Flask, render_template, request, redirect, Response, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY="claveSecretaaa83748"
)  # Secret key para el uso de los formularios
# Para la conexión con la base de datos
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "hallando_huellas"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("index.html")


# Creación de formulario
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TelField, SubmitField
from wtforms.validators import DataRequired, Length

class RegisterUserForm(FlaskForm):
    # Campo de formulario = Clase Tipo Input(Valor de label, validaciones)
    # DataRequired hace que el campo sea necesario completar para poder enviar el formulario (campo obligatorio)
    name = StringField("Nombre: ", validators=[DataRequired()])
    surname = StringField("Apellido: ", validators=[DataRequired()])
    address = StringField("Domicilio: ", validators=[DataRequired()])
    phone = TelField("Teléfono: ", validators=[DataRequired(), Length(min=7, max=15)])
    email = EmailField("Correo electrónico: ", validators=[DataRequired()])
    # Probablemente ponga otra vez la contraseña para confirmar. Para eso se puede usar el validator EqualTo
    password = PasswordField(
        "Contraseña: ", validators=[DataRequired(), Length(min=8, max=20)]
    )
    submit = SubmitField("Registrarse")


# Registrar usuario
@app.route("/auth/register", methods=["GET", "POST"])
def register():
    # Crea una instancia/objeto de la clase para enviar el formulario al template
    form = RegisterUserForm()
    # Si el formulario se envía y es válido se procesan los datos
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        address = form.address.data
        phone = form.phone.data
        email = form.email.data
        password = form.password.data
        return f"Nombre: {name}. Apellido: {surname}. Domicilio: {address}. Teléfono: {phone}. Correo: {email}. Contraseña: {password}"

    # FORMA DE HACERLO SIN WTFORMS
    # if request.method == "POST":
    #     # si se envió el formulario se capturen los datos
    #     # y se almacenen en las variables correspondientes
    #     name = request.form["name"]
    #     surname = request.form["surname"]
    #     address = request.form["address"]
    #     phone = request.form["phone"]
    #     email = request.form["email"]
    #     password = request.form["password"]
    #     if (
    #         len(password) <= 20
    #         and len(password) >= 8
    #         and phone.isdecimal()
    #         and len(phone) > 6
    #     ):
    #         return f"Nombre: {name}. Apellido: {surname}. Domicilio: {address}. Teléfono: {phone}. Correo: {email}. Contraseña: {password}"
    #     else:
    #         error = "El telefono debe ser númerico y mayor a 6 caracteres. Contraseña debe tener de 8 a 20 caracteres."
    #         return render_template("auth/register.html", form=form, error=error)
    return render_template("auth/register.html", form=form)
