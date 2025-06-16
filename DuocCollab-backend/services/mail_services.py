import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')



def enviar_correo_recuperacion(destinatario, nueva_contrasena):
    try:

        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = destinatario
        msg['Subject'] = 'Recuperación de Contraseña'

        cuerpo = f"""
        Hola,\n
        Se ha solicitado una recuperación de contraseña para tu cuenta.\n
        Tu nueva contraseña es: {nueva_contrasena}\n
        Te recomendamos cambiarla después de iniciar sesión.
        
        Para cambiar contraseña debes:
        1) Iniciar sesión con la contraseña entregada en este correo.
        2) Ir a mi perfil.
        3) Ir a Editar perfil.
        4) Crear una nueva contraseña que cumpla con los parámetros.
        5) Guardar los cambios.
        """
        msg.attach(MIMEText(cuerpo, 'plain'))

        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        return True
    except Exception as e:
        print('Error al enviar correo:', e)
        return False