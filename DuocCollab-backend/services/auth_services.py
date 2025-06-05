from flask import jsonify, current_app
from bd.supabase_client import supabase
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token
from services.mail_services import enviar_correo_recuperacion
import random
import string
from .auth_consistencia import (
    guardar_imagen, 
    eliminar_imagen,
    valida_form_login,
    valida_form_usuario,
    validar_carga_img
)


def login_usuario(correo, clave):
    valida_usuario = valida_form_login(correo, clave)
    if valida_usuario != None:
        return(jsonify(valida_usuario)),400

    response = supabase.table('USUARIO').select('*').eq('CORREO',correo).execute()
    usuarios = response.data
    if not usuarios:
        return jsonify({'error':'Correo no registrado'}), 401
    usuario = usuarios[0]
    if not check_password_hash(usuario['CONTRASENIA'], clave):
        return jsonify({'error':'Clave incorrecta'}),401
    access_token = create_access_token(identity=usuario['ID_USUARIO'])

    return jsonify({
        'mensaje':'Login exitoso',
        'usuario':{
            'id':usuario['ID_USUARIO'],
            'nombre':usuario['NOMBRE'],
            'apellido':usuario['APELLIDO'],
            'correo':usuario['CORREO']
        },
        'token':access_token
    })



def registrar_usuario(datos_usuario, archivo_perfil=None, archivo_portada=None):
    errores=[]
    
    """
    REVISAR
    REVISAR
    REVISAR
    REVISAR
    Quitar variables staticas mientras modifican front con SEDE, ESCUELA
    """
    datos_usuario['INTERESES'] = 'Interes por defecto en backend'

    errores = valida_form_usuario(datos_usuario,'crear')
    if errores:
        return {'errores': errores},400
    correo_existe = supabase.table('USUARIO').select('CORREO').eq('CORREO', datos_usuario['CORREO']).execute()
    if correo_existe.data:
        return {'error':'Correo ya existe, Te recomendamos inciar sesión porque ya tienes está cuenta registrada.'}, 409       
    carrera_existe = supabase.table('CARRERA').select('NOMBRE').eq('ID_CARRERA',datos_usuario['ID_CARRERA']).execute()
    if not carrera_existe.data:
        return {'error':'Carrera no existe.'},409

    datos_usuario['CONTRASENIA'] = generate_password_hash(datos_usuario['CONTRASENIA'])
    datos_usuario['FOTO_PERFIL'] = guardar_imagen('perfil', archivo_perfil) if archivo_perfil else 'default_perfil.png'
    datos_usuario['FOTO_PORTADA'] = guardar_imagen('portada', archivo_portada) if archivo_portada else 'default_portada.png'

    response = supabase.table('USUARIO').insert(datos_usuario).execute()
    if not response.data:
        return {"error": "Error al registrar usuario, favor volver a intentar."}, 500

    return {"mensaje": "Usuario registrado con éxito"}, 201




def editar_usuario_servicio(id_usuario, datos_usuario, archivo_perfil=None, archivo_portada=None):
    actualizaciones = {}
    errores=[]



    errores += valida_form_usuario(datos_usuario, modo='editar')
    if archivo_perfil:
        errores += validar_carga_img(archivo_perfil, 'Foto de perfil')
    if archivo_portada:
        errores += validar_carga_img(archivo_portada, 'Foto de portada')
    if errores:
        return {'errores':errores}, 400
    if 'CONTRASENIA' in datos_usuario and datos_usuario['CONTRASENIA']:
        actualizaciones['CONTRASENIA'] = generate_password_hash(datos_usuario['CONTRASENIA'])
    for campo in ['NOMBRE', 'APELLIDO', 'CORREO','INTERESES']:
        if campo in datos_usuario:
            actualizaciones[campo]= datos_usuario[campo].strip()
    
    if 'CORREO' in datos_usuario:
        correo_existe = supabase.table('USUARIO').select('CORREO').eq('CORREO', datos_usuario['CORREO']).neq('ID_USUARIO', id_usuario).execute()
        if correo_existe.data:
            return {'error':'Correo: Se encuentra registrado por otro usuario.'}, 400
    
    if 'ID_CARRERA' in datos_usuario:
        carrera_existe = supabase.table('CARRERA').select('NOMBRE').eq('ID_CARRERA', datos_usuario['ID_CARRERA']).execute()
        if not carrera_existe.data:
            return {'error': 'Carrera no existe.'}, 409
        actualizaciones['ID_CARRERA'] = datos_usuario['ID_CARRERA']
    
    # Obtener datos actuales para eliminar imágenes si corresponde
    usuario_actual = supabase.table("USUARIO").select("FOTO_PERFIL, FOTO_PORTADA").eq("ID_USUARIO", id_usuario).single().execute()
    if not usuario_actual.data:
        return {"error": "Usuario no encontrado"}, 404
    usuario_actual = usuario_actual.data

    if archivo_perfil:
        eliminar_imagen('perfil', usuario_actual.get('FOTO_PERFIL', 'default_perfil.png'))
        actualizaciones['FOTO_PERFIL'] = guardar_imagen('perfil', archivo_perfil)

    if archivo_portada:
        eliminar_imagen('portada', usuario_actual.get('FOTO_PORTADA', 'default_portada.png'))
        actualizaciones['FOTO_PORTADA'] = guardar_imagen('portada', archivo_portada)
    try:
        supabase.table("USUARIO").update(actualizaciones).eq("ID_USUARIO", id_usuario).execute()
        return {"mensaje": "Usuario actualizado correctamente"}, 200
    except Exception as e:
        return {"error": f"Error al actualizar usuario: {str(e)}"}, 500


def obtener_usuario_por_id(id_usuario):
    try:
        resultado = supabase.table("USUARIO").select("*").eq("ID_USUARIO", id_usuario).single().execute()
        if resultado.data:
            return resultado.data, 200
        else:
            return {"error": "Usuario no encontrado"}, 404
    except Exception as e:
        return {"error": f"Error al consultar usuario: {str(e)}"}, 500
    





def restablecer_contrasena(datos):
    correo = datos.get('correo')
    if not correo:
        return {'message','Correo es requerido'}, 400
    resultado = supabase.table("USUARIO").select("*").eq("CORREO", correo).single().execute()
    if not resultado.data:
        return {"error": "Correo no encontrado"}, 404
    
    nueva_pss = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    hash_pss = generate_password_hash(nueva_pss)

    try:
        supabase.table("USUARIO").update({"CONTRASENIA": hash_pss}).eq("CORREO", correo).execute()
        enviar = enviar_correo_recuperacion(correo, nueva_pss)
        if not enviar:
            return {"error": "Error al envia correo."}, 500
        return {"mensaje": f"Contraseña actualizada y reenviada al correo {correo}"}, 200
    except Exception as e:
        return {"error": f"Error al actualizar contraseña: {str(e)}"}, 500
