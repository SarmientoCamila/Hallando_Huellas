import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import qrcode
from io import BytesIO
import base64
from flask import current_app
from .config import Config

# Centraliza la obtención del cursor de MySQL
def get_db_cursor():
    return current_app.extensions['mysql'].connection.cursor()


def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = Config.SMTP_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
        server.starttls()
        server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
        server.send_message(msg)

def generate_qr_code(pet_id):
    base_url = "https://tu-dominio.com/get_mascota/"  # Cambia esto a tu dominio real
    qr_data = f"{base_url}{pet_id}"

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return qr_code_base64
