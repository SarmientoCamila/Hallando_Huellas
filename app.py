from flask import Flask, render_template, request, redirect, session, flash, url_for
import os
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

# Configuración de la base de datos
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
    name = StringField("Nombre", validators=[DataRequired()])
    surname = StringField("Apellido", validators=[DataRequired()])
    address = StringField("Domicilio", validators=[DataRequired()])
    phone = TelField("Teléfono", validators=[DataRequired(), Length(min=7, max=15)])
    email = EmailField("Correo electrónico", validators=[DataRequired()])
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(), EqualTo("confirm_password"), Length(min=8, max=20)],
    )
    confirm_password = PasswordField("Confirmar contraseña", validators=[DataRequired()])
    submit = SubmitField("Registrarse")

# Registro de usuarios
@app.route("/auth/register", methods=["GET", "POST"])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        address = form.address.data
        phone = form.phone.data
        email = form.email.data
        password = form.password.data

        try:
            validate_email(email)
        except Exception as e:
            flash(f"Error al validar el correo: {str(e)}", "error")
            return render_template("auth/register.html", form=form)

        password_hash = hashpw(password.encode("utf-8"), gensalt())
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO users (name, surname, address, phone, email, password_hash) VALUES (%s, %s, %s, %s, %s, %s)",
                (name, surname, address, phone, email, password_hash),
            )
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

# Inicio de sesión
@app.route("/auth/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and checkpw(password.encode("utf-8"), user["password_hash"]):
            session["logged_in"] = True
            session["id_user"] = user["id_user"]
            return redirect("/")
        else:
            flash("Correo electrónico o contraseña incorrecta", "error")
    
    return render_template("auth/login.html", form=form)

# Configuración para subir imágenes
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Ruta para registrar una mascota
@app.route('/pet/mascotas', methods=['GET', 'POST'])
def agregar_mascota():
    error = None
    if request.method == 'POST':
        # Verifica si hay una foto en la solicitud
        if 'foto_mascota' not in request.files:
            flash('No se ha seleccionado ninguna foto', 'error')
            return redirect(request.url)

        foto = request.files['foto_mascota']

        # Verifica si el archivo tiene un nombre
        if foto.filename == '':
            flash('No se ha seleccionado ninguna foto', 'error')
            return redirect(request.url)

        if foto:
            # Guardar la imagen en el servidor
            foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
            foto.save(foto_path)

        # Obtener los demás datos del formulario
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

        if not nombre or not que_mascota or not raza:
            error = "Por favor, completa todos los campos obligatorios."
        else:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO mascotas 
                (nombre, que_mascota, raza, color, anios_mascota, caracteristicas, enfermedades, vacunado, medicamento, castrado, foto_mascota)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (nombre, que_mascota, raza, color, anios_mascota, caracteristicas, enfermedades, vacunado, medicamento, castrado, foto.filename))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('mostrar_mascotas'))  # Redirigir después de agregar

    return render_template("pet/registro_mascota.html", error=error)


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
    cur.execute("SELECT * FROM mascotas WHERE id = %s", [pet_id])
    mascota = cur.fetchone()
    cur.close()
    return render_template('pet/perfil_mascota.html', mascota=mascota)

@app.route('/mascota/<int:pet_id>/editar', methods=['GET', 'POST'])
def editar_mascota(pet_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM mascotas WHERE id = %s", [pet_id])
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
            WHERE id=%s
        """, (nombre, que_mascota, raza, color, anios_mascota, caracteristicas, enfermedades, vacunado, medicamento, castrado, pet_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('mostrar_mascota', pet_id=pet_id))
    
    return render_template('pet/editar_mascota.html', mascota=mascota)

@app.route('/mascota/<int:pet_id>/eliminar', methods=['POST'])
def eliminar_mascota(pet_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM mascotas WHERE id = %s", [pet_id])
    mysql.connection.commit()
    cur.close()
    flash("La mascota ha sido eliminada exitosamente", "success")
    return redirect(url_for('mostrar_mascotas'))

if __name__ == "__main__":
    app.run(debug=True)
