from bd.usuario import obtener_usuarios, crear_usuario, buscar_usuario_por_correo
from werkzeug.security import check_password_hash
import re



def list_usuarios():
    return obtener_usuarios()


def validar_usuario(data):
    errores = []
    nombre = data.get('NOMBRE')
    if not nombre:
        errores.append('El nombre es obligatorio.')
    if not data.get('APELLIDO'):
        errores.append('El apellido es obligatorio.')
    correo = data.get("CORREO","")
    if not correo or not correo.endswith('@duocuc.cl'):
        errores.append('El correo debe tener extensión @duocuc.cl')

    if not data.get("ID_CARRERA"):
        errores.append('El ID de carrera es obligatorio.')
    if not data.get("INTERESES"):
        errores.append('Agregar almenos un interes es obligatorio.')
    
    
    contrasenia = data.get("CONTRASENIA","")
    if len(contrasenia) < 8:
        errores.append("Debe tener al menos 8 caracteres.")

    if correo and correo.split('@')[0].lower() in contrasenia.lower():
        errores.append("No puede contener parte del correo.")
    if nombre and nombre.lower() in contrasenia.lower():
        errores.append("No puede contener el nombre.")
    if not re.search(r'[A-Z]', contrasenia):
        errores.append("Debe tener al menos una letra mayúscula.")
    if not re.search(r'[a-z]', contrasenia):
        errores.append("Debe tener al menos una letra minúscula.")
    if not re.search(r'\d', contrasenia):
        errores.append("Debe tener al menos un número.")
    if not re.search(r'[!@#$%^&*()_\-+=\[\]{};:\'",.<>?/\\|`~]', contrasenia):
        errores.append("Debe tener al menos un símbolo especial.")

    
    
    return errores


def add_usuario(data: dict):
    try:
        errores = validar_usuario(data)
        if errores:
            return {'ok': False, 'errores': errores}, 400 

        correo = data.get('CORREO', '').strip().lower()
        if buscar_usuario_por_correo(correo):
            return {'ok': False, 'errores': ['Ya existe un usuario con este correo.']}, 400

        resp = crear_usuario(data)
        if resp.ok:
            return {'mensaje': 'Usuario creado correctamente'}, 201
        else:
            try:
                error_msg = resp.json().get('error', 'Error desconocido al crear el usuario.')
            except Exception:
                error_msg = resp.text
            return {'error': error_msg}, resp.status_code 

    except Exception as e:
        return {'error': f'Excepción interna: {str(e)}'}, 500
    



def validar_credenciales(correo:str, contrasenia:str):
    usuarios = obtener_usuarios()
    for usuario in usuarios:
        if usuario['CORREO'] == correo and check_password_hash(usuario['CONTRASENIA'],contrasenia):
            return usuario
    return None