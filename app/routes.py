from flask import Blueprint, render_template, request, jsonify, flash, redirect
from bcrypt import hashpw, gensalt, checkpw
from email_validator import validate_email
from .forms import RegisterUserForm, LoginForm
from . import mysql
from .utils import generate_qr_code

main_routes = Blueprint('main', __name__)
auth_routes = Blueprint('auth', __name__)

@main_routes.route("/")
def home():
    return render_template("index.html")

@main_routes.route("/datos_mascota")
def mascota():
    return render_template("datos_mascota.html")

@auth_routes.route("/register", methods=["GET", "POST"])
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
            flash(f"Error al validar: {str(e)}", "error")
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

@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        if user:
            password_hash = user["password_hash"]
            if isinstance(password_hash, bytes) and checkpw(password.encode("utf-8"), password_hash):
                session["logged_in"] = True
                session["id_user"] = user["id_user"]
                return redirect("/")
            else:
                flash("Contraseña incorrecta", "error")
        else:
            flash("Correo electrónico no registrado", "error")
    return render_template("auth/login.html", form=form)

@main_routes.route('/register_mascota', methods=['POST'])
def register_mascota():
    data = request.form  # Cambia de `request.get_json()` a `request.form` para obtener datos de un formulario
    nombre = data.get('nombre')
    id_dueño = data.get('id_dueño')
    descripcion = data.get('descripcion')
    telefono = data.get('telefono')

    # Validar datos
    if not nombre or not id_dueño or not descripcion or not telefono:
        return jsonify({'error': 'Todos los campos son requeridos'}), 400

    try:
        # Insertar la mascota en la base de datos
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO mascotas (nombre, id_dueño, descripcion, telefono) VALUES (%s, %s, %s, %s)",
            (nombre, id_dueño, descripcion, telefono)
        )
        mysql.connection.commit()
        pet_id = cur.lastrowid  # Obtener el ID de la mascota recién insertada
        cur.close()

        # Generar el código QR
        qr_code = generate_qr_code(pet_id)

        # Actualizar la mascota con el código QR
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE mascotas SET qr_code = %s WHERE id = %s",
            (qr_code, pet_id)
        )
        mysql.connection.commit()
        cur.close()

        return jsonify({'qr_code': qr_code}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

    # Endpoint para obtener información de la mascota mediante el escaneo del QR
@main_routes.route('/get_mascota/<int:pet_id>', methods=['GET'])
def get_mascota(pet_id):
    try:
        # Obtener la mascota de la base de datos
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM mascotas WHERE id = %s", (pet_id,))
        mascota = cur.fetchone()
        cur.close()
        
        if not mascota:
            return jsonify({'error': 'Mascota no encontrada'}), 404

        return jsonify({
            'nombre': mascota['nombre'],
            'descripcion': mascota['descripcion']
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

