from flask import Blueprint, request, jsonify, send_from_directory
from services.proyecto_service import *
from .auth import verificar_token
import os
import uuid

proyecto_bp = Blueprint('proyecto', __name__)
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads', 'imagenes_proyectos'))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def generar_nombre_archivo(nombre_original):
    extension = os.path.splitext(nombre_original)[1]
    return f"{uuid.uuid4().hex}{extension}"


def guardar_archivo(nombre):
    return '.' in nombre and nombre.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Imagen proyecto
@proyecto_bp.route('/api/uploads/imagen_proyecto/<filename>', methods=['GET'])
def obtener_imagen(filename):
    verificar_token()
    return send_from_directory(UPLOAD_FOLDER, filename)


# Proyectos
@proyecto_bp.route('/api/proyectos', methods=['GET', 'POST'])
def proyectos():
    verificar_token()
    
    if request.method == 'GET':
        return jsonify(list_proyectos())

    if request.content_type.startswith('multipart/form-data'):
        datos = request.form.to_dict()
        archivos = request.files

        archivo = archivos.get('FOTO_PROYECTO')
        if archivo and archivo.filename and guardar_archivo(archivo.filename):
            filename = generar_nombre_archivo(archivo.filename)
            archivo.save(os.path.join(UPLOAD_FOLDER, filename))
            datos['FOTO_PROYECTO'] = filename
        else:
            datos['FOTO_PROYECTO'] = None

        resp_json, status_code = add_proyecto(datos)
        return jsonify(resp_json), status_code

    return jsonify({'error': 'Tipo de contenido no soportado. Usa multipart/form-data.'}), 415


# Mis Proyectos (filtrados por usuario que hace la solicitud)
@proyecto_bp.route('/api/mis-proyectos', methods=['GET'])
def mis_proyectos():
    id_usuario = verificar_token()

    proyectos = obtener_proyectos_por_usuario(id_usuario)
    return jsonify(proyectos), 200


# Etiquetas
@proyecto_bp.route('/api/etiquetas', methods=['GET', 'POST'])
def etiquetas():
    verificar_token()

    if request.method == 'GET':
        return jsonify(list_etiquetas())

    resp = add_etiqueta(request.json)
    if resp.ok:
        return jsonify({'mensaje': 'Etiqueta creada'}), 201
    return jsonify({'error': resp.text}), resp.status_code


# Integrantes de proyecto
@proyecto_bp.route('/api/integrantesProyectos', methods=['GET', 'POST'])
def integrantes():
    verificar_token()

    if request.method == 'GET':
        return jsonify(list_integrantes())

    resp = add_integrante(request.json)
    if resp.ok:
        return jsonify({'mensaje': 'Integrante añadido'}), 201
    return jsonify({'error': resp.text}), resp.status_code


# Postulaciones
@proyecto_bp.route('/api/postulantes', methods=['GET', 'POST'])
def postulantes():
    verificar_token()

    if request.method == 'GET':
        return jsonify(list_postulaciones())

    resp = add_postulacion(request.json)
    if resp.ok:
        return jsonify({'mensaje': 'Postulación creada'}), 201
    return jsonify({'error': resp.text}), resp.status_code


# Proyecto - Etiqueta
@proyecto_bp.route('/api/proyectoEtiqueta', methods=['GET', 'POST'])
def proyecto_etiqueta():
    verificar_token()

    if request.method == 'GET':
        return jsonify(list_proyecto_etiqueta())

    resp = add_proyecto_etiqueta(request.json)
    if resp.ok:
        return jsonify({'mensaje': 'Etiqueta vinculada'}), 201
    return jsonify({'error': resp.text}), resp.status_code
