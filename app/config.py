
# app/config.py
class Config:
    SECRET_KEY = "claveSecretaaa83748"
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "Hhpassword"
    MYSQL_DB = "hallando_huellas"
    MYSQL_CURSORCLASS = "DictCursor"



  
      # SMTP Configurations for Mailtrap
    SMTP_SERVER = 'sandbox.smtp.mailtrap.io'
    SMTP_PORT = 587  # Se puede usar 25, 465, 587 o 2525
    SMTP_USER = '61f2f1b236dcd1'
    SMTP_PASSWORD = '357fb9a1c889bb'  