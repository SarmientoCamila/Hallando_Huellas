from flask import Flask, render_template, request, redirect, Response, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TelField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_mysqldb import MySQL
from bcrypt import hashpw, gensalt, checkpw
from email_validator import validate_email


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


# Creación de formulario de registro
class RegisterUserForm(FlaskForm):
    # Campo de formulario = Clase Tipo Input(Valor de label, validaciones)
    # DataRequired hace que el campo sea obligatorio
    name = StringField("Nombre", validators=[DataRequired()])
    surname = StringField("Apellido", validators=[DataRequired()])
    address = StringField("Domicilio", validators=[DataRequired()])
    phone = TelField("Teléfono", validators=[DataRequired(), Length(min=7, max=15)])
    email = EmailField("Correo electrónico", validators=[DataRequired()])
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(), EqualTo("confirm_password"), Length(min=8, max=20)],
    )
    confirm_password = PasswordField(
        "Confirmar contraseña", validators=[DataRequired()]
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

        # Validar email
        try:
            validate_email(email)
        except Exception as e:
            flash(f"Error al validar: {str(e)}", "error")
            return render_template("/auth/register.html", form=form)

        # Encriptar contraseña (Hashear)
        password_hash = hashpw(password.encode("utf-8"), gensalt())
        try:
            # Se insertan los datos en la base de datos.
            # Un cursor es un objeto. Ejecuta comandos SQL
            # y obtiene los resultados de las consultas.
            cur = mysql.connection.cursor()

            # execute() ejecuta la consulta
            cur.execute(
                "INSERT INTO users (name, surname, address, phone, email, password_hash) VALUES (%s, %s, %s, %s, %s, %s)",
                (name, surname, address, phone, email, password_hash),
            )

            # commit() confirma los cambios en la base de datos
            # cur.close() cierra el cursor luego de ejecutar la consulta
            mysql.connection.commit()
            cur.close()

            return redirect("/")
        except Exception as e:
            flash(f"Error al registrar usuario: {str(e)}", "error")

    return render_template("auth/register.html", form=form)


# Creación de formulario de inicio de sesión
class LoginForm(FlaskForm):
    email = EmailField("Correo electrónico", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar sesión")
    # Se puede poner un BooleanField para recordar contraseña, habría que importarlo.


# Iniciar sesión
@app.route("/auth/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Buscar usuario en base de datos
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        if user:
            # Validar contraseña
            password_hash = user["password_hash"]
            if isinstance(password_hash, bytes) and checkpw(
                password.encode("utf-8"), password_hash
            ):
                # Se inicia sesión
                session["logged_in"] = True
                session["id_user"] = user["id_user"]
                return redirect("/")
            else:
                flash("Contraseña incorrecta", "error")
        else:
            flash("Correo electrónico no registrado", "error")
    return render_template("auth/login.html", form=form)


@app.route("/datos_mascota")
def mascota():
    return render_template("datos_mascota.html")


if __name__ == "__main__":
    app.run(debug=True)


# FORMA DE HACERLO SIN WTFORMS
# if request.method == "POST":
# si se envió el formulario se capturen los datos, se almacenen en las variables correspondientes
#     name = request.form["name"]
#     surname = request.form["surname"]
#     address = request.form["address"]
#     phone = request.form["phone"]
#     email = request.form["email"]
#     password_hash = request.form["password_hash"]
#     if (
#         len(password_hash) <= 20
#         and len(password_hash) >= 8
#         and phone.isdecimal()
#         and len(phone) > 6
#     ):
#         return f"Nombre: {name}. Apellido: {surname}. Domicilio: {address}. Teléfono: {phone}. Correo: {email}. Contraseña: {password_hash}"
#     else:
#         error = "El telefono debe ser númerico y mayor a 6 caracteres. Contraseña debe tener de 8 a 20 caracteres."
#         return render_template("auth/register.html", form=form, error=error)
