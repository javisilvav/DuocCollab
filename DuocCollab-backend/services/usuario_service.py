from bd.usuario import obtener_usuarios, crear_usuario, buscar_usuario_por_correo, modificar_usuario, obtener_usuario_por_id
from werkzeug.security import check_password_hash
import re



def list_usuarios():
    return obtener_usuarios()


import re

def validar_usuario(data, modo='crear'):
    errores = []

    nombre = data.get('NOMBRE')
    if modo == 'crear' or 'NOMBRE' in data:
        if not nombre or not nombre.strip():
            errores.append('El nombre es obligatorio.')

    apellido = data.get('APELLIDO')
    if modo == 'crear' or 'APELLIDO' in data:
        if not apellido or not apellido.strip():
            errores.append('El apellido es obligatorio.')

    correo = data.get("CORREO")
    if modo == 'crear' or 'CORREO' in data:
        if not correo or not correo.endswith('@duocuc.cl'):
            errores.append('El correo debe tener extensión @duocuc.cl')

    if modo == 'crear' or 'ID_CARRERA' in data:
        if not data.get("ID_CARRERA"):
            errores.append('El ID de carrera es obligatorio.')

    if modo == 'crear' or 'INTERESES' in data:
        intereses = data.get("INTERESES")
        if not intereses or not isinstance(intereses, list) or len(intereses) == 0:
            errores.append('Agregar al menos un interés es obligatorio.')

    contrasenia = data.get("CONTRASENIA")
    if modo == 'crear' or contrasenia:
        if not contrasenia:
            errores.append("La contraseña es obligatoria.")
        else:
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
        errores = validar_usuario(data, modo='crear')
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



def update_usuario(id_usuario: int, data: dict):
    try:
        usuario_actual = obtener_usuario_por_id(id_usuario)
        if not usuario_actual:
            return {'error': 'Usuario no encontrado'}, 404

        errores = validar_usuario(data, modo='editar')
        if errores:
            return {'ok': False, 'errores': errores}, 400

        if not data.get('CONTRASENA'):
            data['CONTRASENA'] = None

        resp = modificar_usuario(id_usuario, data)
        if resp.ok:
            return {'mensaje': 'Usuario actualizado correctamente'}, 200
        else:
            return {'error': resp.text}, resp.status_code

    except Exception as e:
        return {'error': f'Excepción interna: {str(e)}'}, 500