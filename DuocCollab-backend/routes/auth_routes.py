from flask import Blueprint, request, jsonify, send_from_directory
from services.auth_services import (
    login_usuario, 
    registrar_usuario,
    editar_usuario_servicio, 
    obtener_usuario_por_id, 
    restablecer_contrasena,
    obtener_correos,
    contar_usuarios,
    obtener_usuarios_registrados
)
from services.auth_consistencia import trae_ruta_imagen
from flask_jwt_extended import jwt_required, get_jwt_identity



auth_bp = Blueprint('auth_bp',__name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data=request.get_json()
    correo=data.get('correo')
    clave=data.get('clave')
    return login_usuario(correo, clave)


@auth_bp.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    if not datos:
        return jsonify({'error':'Debe enviar JSON con los datos'}), 400
    resultado, status = registrar_usuario(datos)
    return jsonify(resultado), status


@auth_bp.route('/editar', methods=['PUT'])
@jwt_required()
def editar_usuario():
    id_usuario = get_jwt_identity()
    datos = request.form.to_dict()
    imagen_perfil = request.files.get('FOTO_PERFIL')
    imagen_portada = request.files.get('FOTO_PORTADA')

    resultado, status = editar_usuario_servicio(id_usuario=id_usuario, datos_usuario=datos, archivo_perfil=imagen_perfil, archivo_portada=imagen_portada)
    return jsonify(resultado), status



@auth_bp.route('/usuario_actual', methods=['GET'])
@jwt_required()
def obtener_usuario_actual():
    id_usuario = get_jwt_identity()
    usuario, status = obtener_usuario_por_id(id_usuario)
    return jsonify(usuario), status


@auth_bp.route('/imagen/<tipo>/<nombre>')
#@jwt_required()
def obtener_imagen(tipo, nombre):
    if tipo not in ['perfil', 'portada']:
        return {"error": "Tipo inválido"}, 400
    
    carpeta = trae_ruta_imagen(tipo)
    #print(f"[DEBUG] Buscando imagen en: {carpeta}, archivo: {nombre}")

    try:
        return send_from_directory(carpeta, nombre)
    except FileNotFoundError:
        return jsonify({"error": "Archivo no encontrado"}), 404
    



@auth_bp.route('/recuperar_contrasena', methods=['POST'])
def recuperar_contrasena():
    datos = request.get_json()
    contrasena, status = restablecer_contrasena(datos)
    return jsonify(contrasena),status




@auth_bp.route('/correos', methods=['GET'])
@jwt_required()
def obtener_correo():
    correo, status = obtener_correos()
    return jsonify(correo), status

@auth_bp.route('/usuarios_registrados', methods=['GET'])
@jwt_required()
def obtener_usuarios():
    usuarios, status = obtener_usuarios_registrados()
    return jsonify(usuarios), status


@auth_bp.route('/count_user', methods=['GET'])
@jwt_required()
def count_usuarios():
    cant_usuario, status = contar_usuarios()
    return jsonify(cant_usuario), status