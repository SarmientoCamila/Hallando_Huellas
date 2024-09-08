# app/config.py
class Config:
    SECRET_KEY = "claveSecretaaa83748"
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = ""
    MYSQL_DB = "hallando_huellas"
    MYSQL_CURSORCLASS = "DictCursor"


  
    # SMTP Configurations
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USER = 'tu_email@gmail.com'
    SMTP_PASSWORD = 'tu_contraseña'