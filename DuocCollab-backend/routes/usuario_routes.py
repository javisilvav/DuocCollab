from flask import Blueprint, request, jsonify, send_from_directory
from services.usuario_service import list_usuarios, add_usuario, validar_credenciales
from .auth import generar_token, verificar_token
import os
import uuid

usuario_bp = Blueprint('usuario', __name__)

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads', 'imagenes'))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def generar_nombre_archivo(nombre_original):
    extension = os.path.splitext(nombre_original)[1]
    return f"{uuid.uuid4().hex}{extension}"


def guardar_archivo(nombre):
    return '.' in nombre and nombre.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@usuario_bp.route('/api/uploads/imagenes/<filename>', methods=['GET'])
def obtener_imagen(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@usuario_bp.route('/api/usuarios', methods=['GET', 'POST'])
def usuarios():
    id_usuario = verificar_token()  

    if request.method == 'GET':
        return jsonify(list_usuarios())

    # POST con multipart/form-data (con archivos)
    if request.content_type.startswith('multipart/form-data'):
        datos = request.form.to_dict()
        archivos = request.files

        for campo in ['FOTO_PERFIL', 'FOTO_PORTADA']:
            archivo = archivos.get(campo)
            if archivo and archivo.filename and guardar_archivo(archivo.filename):
                filename = generar_nombre_archivo(archivo.filename)
                archivo.save(os.path.join(UPLOAD_FOLDER, filename))
                datos[campo] = filename
            else:
                datos[campo] = None

        resp_json, status_code = add_usuario(datos)
        return jsonify(resp_json), status_code

    return jsonify({'error': 'Tipo de contenido no soportado. Usa multipart/form-data.'}), 415

@usuario_bp.route('/api/login', methods=['POST'])
def login_usuario():
    data = request.json
    correo = data.get('CORREO')
    contrasenia = data.get('CONTRASENIA')

    if not correo or not contrasenia:
        return jsonify({'error': 'Correo y contraseña requeridos'}), 400

    usuario = validar_credenciales(correo, contrasenia)
    if usuario:
        token = generar_token(usuario['ID_USUARIO'])
        return jsonify({'token': token, 'usuario': usuario}), 200

    return jsonify({'error': 'Credenciales inválidas'}), 401
