# import unittest
# from unittest.mock import patch, MagicMock
# from flask import json
# from app import create_app
# from app.utils import send_email, generate_qr_code

# class FlaskTestCase(unittest.TestCase):
#     def setUp(self):
#         # Configura la aplicación para pruebas
#         self.app = create_app()
#         self.app.config['TESTING'] = True
#         self.app.config['WTF_CSRF_ENABLED'] = False
#         self.client = self.app.test_client()

#     # Test para la ruta home
#     def test_home(self):
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)

#     # Test para registro de usuario
#     @patch('app.routes.mysql.connection.cursor')
#     def test_register_user(self, mock_cursor):
#         mock_cursor.return_value.fetchone.return_value = None  # Simula que no hay un usuario registrado

#         data = {
#             'name': 'John',
#             'surname': 'Doe',
#             'address': '123 Calle Falsa',
#             'phone': '123456789',
#             'email': 'john@example.com',
#             'password': 'password123',
#             'confirm_password': 'password123'
#         }
#         response = self.client.post('/auth/register', data=data, follow_redirects=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b'Registrarse', response.data)

#     # Test para login de usuario
#     @patch('app.routes.mysql.connection.cursor')
#     def test_login_user(self, mock_cursor):
#         mock_cursor.return_value.fetchone.return_value = {
#             'email': 'john@example.com',
#             'password_hash': b'$2b$12$KixqNw...'
#         }  # Simulando un hash válido

#         data = {
#             'email': 'john@example.com',
#             'password': 'password123'
#         }
#         response = self.client.post('/auth/login', data=data, follow_redirects=True)
#         self.assertEqual(response.status_code, 200)

#     # Test para registro de mascota
#     @patch('app.routes.mysql.connection.cursor')
#     @patch('app.utils.generate_qr_code')
#     def test_register_mascota(self, mock_generate_qr_code, mock_cursor):
#         mock_generate_qr_code.return_value = 'mock_qr_code'
#         mock_cursor.return_value.lastrowid = 1  # Simula que se insertó un ID de mascota

#         data = {
#             'nombre': 'Firulais',
#             'id_dueño': 1,
#             'descripcion': 'Perro de raza',
#             'telefono': '123456789'
#         }
#         response = self.client.post('/register_mascota', data=data)
#         self.assertEqual(response.status_code, 201)
#         self.assertIn(b'mock_qr_code', response.data)

#     # Test para obtener mascota
#     @patch('app.routes.mysql.connection.cursor')
#     def test_get_mascota(self, mock_cursor):
#         mock_cursor.return_value.fetchone.return_value = {
#             'nombre': 'Firulais',
#             'descripcion': 'Perro de raza'
#         }

#         response = self.client.get('/get_mascota/1')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b'Firulais', response.data)

#     # Test para contacto de mascota
#     @patch('app.routes.mysql.connection.cursor')
#     def test_contacto(self, mock_cursor):
#         mock_cursor.return_value.fetchone.return_value = {
#             'telefono': '123456789'
#         }

#         response = self.client.get('/contacto/1')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b'123456789', response.data)

#     # Test para reportar ubicación
#     @patch('app.routes.mysql.connection.cursor')
#     @patch('app.utils.send_email')
#     def test_report_location(self, mock_send_email, mock_cursor):
#         mock_cursor.return_value.fetchone.return_value = {
#             'dueño': 'owner@example.com'
#         }

#         data = {
#             'pet_id': 1,
#             'latitude': 40.7128,
#             'longitude': -74.0060
#         }
#         response = self.client.post('/contact/report_location', json=data)
#         self.assertEqual(response.status_code, 200)
#         mock_send_email.assert_called_with(
#             'dueño@ejemplo.com',
#             'Ubicación de Mascota',
#             'La mascota con ID 1 ha sido encontrada en la siguiente ubicación:\n\nLatitud: 40.7128\nLongitud: -74.0060'
#         )

#     # Test para reportar dirección
#     @patch('app.routes.mysql.connection.cursor')
#     @patch('app.utils.send_email')
#     def test_report_address(self, mock_send_email, mock_cursor):
#         mock_cursor.return_value.fetchone.return_value = {
#             'dueño': 'owner@example.com'
#         }

#         data = {
#             'pet_id': 1,
#             'address': '123 Calle Falsa'
#         }
#         response = self.client.post('/contact/report_address', json=data)
#         self.assertEqual(response.status_code, 200)
#         mock_send_email.assert_called_with(
#             'dueño@ejemplo.com',
#             'Dirección de Mascota',
#             'La mascota con ID 1 ha sido encontrada en la siguiente dirección:\n\n123 Calle Falsa'
#         )

# if __name__ == '__main__':
#     unittest.main()
