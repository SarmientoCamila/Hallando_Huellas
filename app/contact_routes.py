from flask import Blueprint, request, jsonify
from .utils import send_email, get_db_cursor  # Importar función desde utils.py

contact_routes = Blueprint('contact', __name__)

@contact_routes.route('/contacto/<int:pet_id>', methods=['GET'])
def contacto(pet_id):
    try:
        cur = get_db_cursor()  # Usa la función para obtener el cursor
        cur.execute("SELECT telefono FROM mascotas WHERE id = %s", (pet_id,))
        mascota = cur.fetchone()
        cur.close()

        if not mascota:
            return jsonify({'error': 'Mascota no encontrada'}), 404

        return jsonify({'telefono': mascota['telefono']}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@contact_routes.route('/report_location', methods=['POST'])
def report_location():
    data = request.get_json()
    pet_id = data.get('pet_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    cur = get_db_cursor()  # Usa la función para obtener el cursor
    cur.execute("SELECT dueño FROM mascotas WHERE id = %s", (pet_id,))
    mascota = cur.fetchone()
    cur.close()

    if not mascota:
        return jsonify({'error': 'Mascota no encontrada'}), 404

    # Aquí debes obtener el correo electrónico del dueño desde otra fuente si no está en la tabla mascota
    dueño_email = 'dueño@ejemplo.com'  # Cambia esto a la consulta real

    subject = 'Ubicación de Mascota'
    body = f'La mascota con ID {pet_id} ha sido encontrada en la siguiente ubicación:\n\nLatitud: {latitude}\nLongitud: {longitude}'

    send_email(dueño_email, subject, body)
    
    return jsonify({'message': 'Ubicación recibida y correo enviado exitosamente'}), 200

@contact_routes.route('/report_address', methods=['POST'])
def report_address():
    data = request.get_json()
    pet_id = data.get('pet_id')
    address = data.get('address')
    cur = get_db_cursor()  # Usa la función para obtener el cursor
    pet_id = data.get('pet_id')
    address = data.get('address')

    cur = get_db_cursor()  # Usa la función para obtener el cursor
    cur.execute("SELECT dueño FROM mascotas WHERE id = %s", (pet_id,))
    mascota = cur.fetchone()
    cur.close()

    if not mascota:
        return jsonify({'error': 'Mascota no encontrada'}), 404

    # Aquí debes obtener el correo electrónico del dueño desde otra fuente si no está en la tabla mascota
    dueño_email = 'dueño@ejemplo.com'  # Cambia esto a la consulta real

    subject = 'Dirección de Mascota'
    body = f'La mascota con ID {pet_id} ha sido encontrada en la siguiente dirección:\n\n{address}'

    send_email(dueño_email, subject, body)
    
    return jsonify({'message': 'Dirección recibida y correo enviado exitosamente'}), 200
