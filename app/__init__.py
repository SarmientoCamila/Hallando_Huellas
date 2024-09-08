# app/__init__.py
from flask import Flask
from flask_mysqldb import MySQL
from .config import Config
from .routes import main_routes, auth_routes
from .contact_routes import contact_routes  # Importa los nuevos routes


mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mysql.init_app(app)
    
    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes, url_prefix='/auth')
    app.register_blueprint(contact_routes, url_prefix='/contact')  # Asegúrate de registrar el blueprint correctamente

    return app
