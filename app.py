<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, session, flash, url_for
=======
from flask import Flask, render_template, request, redirect, Response, session, flash
>>>>>>> b2666a97e8d3db46af6399e7b6e1414ff9efbc25
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TelField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_mysqldb import MySQL
from bcrypt import hashpw, gensalt, checkpw
from email_validator import validate_email
<<<<<<< HEAD
import os
from werkzeug.utils import secure_filename

=======
>>>>>>> b2666a97e8d3db46af6399e7b6e1414ff9efbc25


app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY="claveSecretaaa83748"
)  # Secret key para el uso de los formularios
<<<<<<< HEAD

# Configuración de la base de datos
=======
# Para la conexión con la base de datos
>>>>>>> b2666a97e8d3db46af6399e7b6e1414ff9efbc25
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "hallando_huellas"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

<<<<<<< HEAD
=======

>>>>>>> b2666a97e8d3db46af6399e7b6e1414ff9efbc25
@app.route("/")
def home():
    return render_template("index.html")

<<<<<<< HEAD
# Creación de formulario de registro
class RegisterUserForm(FlaskForm):
=======

# Creación de formulario de registro
class RegisterUserForm(FlaskForm):
    # Campo de formulario = Clase Tipo Input(Valor de label, validaciones)
    # DataRequired hace que el campo sea obligatorio
>>>>>>> b2666a97e8d3db46af6399e7b6e1414ff9efbc25
    name = StringField("Nombre", validators=[DataRequired()])
    surname = StringField("Apellido", validators=[DataRequired()])
    address = StringField("Domicilio", validators=[DataRequired()])
    phone = TelField("Teléfono", validators=[DataRequired(), Length(min=7, max=15)])
    email = EmailField("Correo electrónico", validators=[DataRequired()])
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(), EqualTo("confirm_password"), Length(min=8, max=20)],
    )
<<<<<<< HEAD
    confirm_password = PasswordField("Confirmar contraseña", validators=[DataRequired()])
    submit = SubmitField("Registrarse")

# Registro de usuarios
@app.route("/auth/register", methods=["GET", "POST"])
def register():
    form = RegisterUserForm()
=======
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
>>>>>>> b2666a97e8d3db46af6399e7b6e1414ff9efbc25
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        address = form.address.data
        phone = form.phone.data
        email = form.email.data
        password = form.password.data

<<<<<<< HEAD
        try:
            validate_email(email)
        except Exception as e:
            flash(f"Error al validar el correo: {str(e)}", "error")
            return render_template("auth/register.html", form=form)

        password_hash = hashpw(password.encode("utf-8"), gensalt())
        try:
            cur = mysql.connection.cursor()
=======
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
>>>>>>> b2666a97e8d3db46af6399e7b6e1414ff9efbc25
            cur.execute(
                "INSERT INTO users (name, surname, address, phone, email, password_hash) VALUES (%s, %s, %s, %s, %s, %s)",
                (name, surname, address, phone, email, password_hash),
            )
<<<<<<< HEAD
            mysql.connection.commit()
            cur.close()
=======

            # commit() confirma los cambios en la base de datos
            # cur.close() cierra el cursor luego de ejecutar la consulta
            mysql.connection.commit()
            cur.close()

>>>>>>> b2666a97e8d3db46af6399e7b6e1414ff9efbc25
            return redirect("/")
        except Exception as e:
            flash(f"Error al registrar usuario: {str(e)}", "error")

    return render_template("auth/register.html", form=form)

<<<<<<< HEAD
=======

>>>>>>> b2666a97e8d3db46af6399e7b6e1414ff9efbc25
# Creación de formulario de inicio de sesión
class LoginForm(FlaskForm):
    email = EmailField("Correo electrónico", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar sesión")
<<<<<<< HEAD

# Inicio de sesión
=======
    # Se puede poner un BooleanField para recordar contraseña, habría que importarlo.


# Iniciar sesión
>>>>>>> b2666a97e8d3db46af6399e7b6e1414ff9efbc25
@app.route("/auth/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

<<<<<<< HEAD
=======
        # Buscar usuario en base de datos
>>>>>>> b2666a97e8d3db46af6399e7b6e1414ff9efbc25
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
<<<<<<< HEAD

        if user and checkpw(password.encode("utf-8"), user["password_hash"]):
            session["logged_in"] = True
            session["id_user"] = user["id_user"]
            return redirect("/")
        else:
            flash("Correo electrónico o contraseña incorrecta", "error")
    
    return render_template("auth/login.html", form=form)





# Configuración para la subida de archivos
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Carpeta donde se almacenarán las imágenes subidas
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Límite de 16MB para las subidas de archivos

# Rutas permitidas para subir archivos (extensiones permitidas)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





# Ruta para registrar una mascota
@app.route('/mascota/nueva', methods=['GET', 'POST'])
def agregar_mascota():
    if request.method == 'POST':
        nombre = request.form['nombre']
        que_mascota = request.form['que_mascota']
        raza = request.form['raza']
        color = request.form['color']
        anios_mascota = request.form['anios_mascota']
        caracteristicas = request.form['caracteristicas']
        enfermedades = request.form['enfermedades']
        vacunado = request.form.get('vacunado') == 'on'
        medicamento = request.form['medicamento']
        castrado = request.form.get('castrado') == 'on'

        # Verifica si se ha subido un archivo de imagen
        if 'foto_mascota' not in request.files:
            flash('No se subió ningún archivo')
            return redirect(request.url)

        file = request.files['foto_mascota']
        if file.filename == '':
            flash('No se seleccionó ninguna imagen')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Inserta los datos en la base de datos, incluyendo la imagen
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO mascotas (nombre, que_mascota, raza, color, anios_mascota, caracteristicas, enfermedades, vacunado, medicamento, castrado, foto_mascota) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (nombre, que_mascota, raza, color, anios_mascota, caracteristicas, enfermedades, vacunado, medicamento, castrado, filename))
            mysql.connection.commit()
            cur.close()

            flash('Mascota registrada con éxito')
            return redirect(url_for('mostrar_mascotas'))

    return render_template('pet/registro_mascota.html')

# Rutas para mostrar, editar y eliminar mascotas
@app.route('/mostrar_mascotas')
def mostrar_mascotas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM mascotas")
    mascotas = cur.fetchall()
    cur.close()
    return render_template('pet/mostrar_mascotas.html', mascotas=mascotas)

@app.route('/mascota/<int:pet_id>', methods=['GET'])
def mostrar_mascota(pet_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM mascotas WHERE pet_id = %s", [pet_id])
    mascota = cur.fetchone()
    cur.close()
    return render_template('pet/perfil_mascota.html', mascota=mascota)

@app.route('/mascota/<int:pet_id>/editar', methods=['GET', 'POST'])
def editar_mascota(pet_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM mascotas WHERE pet_id = %s", [pet_id])
    mascota = cur.fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        que_mascota = request.form['que_mascota']
        raza = request.form['raza']
        color = request.form['color']
        anios_mascota = request.form['anios_mascota']
        caracteristicas = request.form['caracteristicas']
        enfermedades = request.form['enfermedades']
        vacunado = request.form.get('vacunado') == 'on'
        medicamento = request.form['medicamento']
        castrado = request.form.get('castrado') == 'on'
        
        cur.execute("""
            UPDATE mascotas 
            SET nombre=%s, que_mascota=%s, raza=%s, color=%s, anios_mascota=%s, caracteristicas=%s, enfermedades=%s, vacunado=%s, medicamento=%s, castrado=%s 
            WHERE pet_id=%s
        """, (nombre, que_mascota, raza, color, anios_mascota, caracteristicas, enfermedades, vacunado, medicamento, castrado, pet_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('mostrar_mascota', pet_id=pet_id))
    
    return render_template('pet/editar_mascota.html', mascota=mascota)

@app.route('/mascota/<int:pet_id>/eliminar', methods=['POST'])
def eliminar_mascota(pet_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM mascotas WHERE pet_id = %s", [pet_id])
    mysql.connection.commit()
    cur.close()
    flash("La mascota ha sido eliminada exitosamente", "success")
    return redirect(url_for('mostrar_mascotas'))

if __name__ == "__main__":
    app.run(debug=True)
=======
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
>>>>>>> b2666a97e8d3db46af6399e7b6e1414ff9efbc25
