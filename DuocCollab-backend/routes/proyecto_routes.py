from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, send_from_directory
from services.proyecto_consistencia import trae_ruta_imagen
from services.proyecto_services import (
    obtener_proyecto_usuario,
    cargar_proyecto,
    obtener_postulacion_usuario,
    cargar_postulacion,
    obtener_detalle_proyecto,
    obtener_proyetos,
    editar_estado_postulacion,
    obtener_etiquetas,

)



proyecto_bp = Blueprint('proyecto_bp',__name__, url_prefix='/api/proyecto')



@proyecto_bp.route('/imagen/<tipo>/<nombre>')
#@jwt_required()
def obtener_imagen(tipo, nombre):
    if tipo not in ['proyecto']:
        return {"error": "Tipo inválido"}, 400
    
    carpeta = trae_ruta_imagen(tipo)
    #print(f"[DEBUG] Buscando imagen en: {carpeta}, archivo: {nombre}")

    try:
        return send_from_directory(carpeta, nombre)
    except FileNotFoundError:
        return jsonify({"error": "Archivo no encontrado"}), 404
    


@proyecto_bp.route('/crear_postulacion', methods=['POST'])
@jwt_required()
def crear_postulacion():
    id_usuario = get_jwt_identity()
    datos = request.get_json()
    resultado, status = cargar_postulacion(id_usuario, datos)
    return jsonify(resultado), status

@proyecto_bp.route('/mis_postulaciones', methods=['GET'])
@jwt_required()
def postulaciones_usuario():
    id_usuario = get_jwt_identity()
    proyectos, status = obtener_postulacion_usuario(id_usuario)
    return jsonify(proyectos), status


@proyecto_bp.route('/editar_postulacion', methods=['POST'])
@jwt_required()
def estado_postulacion():
    datos = request.get_json()
    proyectos, status = editar_estado_postulacion(datos)
    return jsonify(proyectos), status


@proyecto_bp.route('/detalle_proyecto', methods=['GET'])
@jwt_required()
def detalle_proyecto():
    data_proyecto = request.get_json()
    proyectos, status = obtener_detalle_proyecto(data_proyecto)
    return jsonify(proyectos), status


@proyecto_bp.route('/proyectos', methods=['GET'])
@jwt_required()
def proyectos():
    proyectos, status = obtener_proyetos()
    return jsonify(proyectos), status

@proyecto_bp.route('/mis_proyectos', methods=['GET'])
@jwt_required()
def proyectos_usuario():
    id_usuario = get_jwt_identity()
    proyectos, status = obtener_proyecto_usuario(id_usuario)
    return jsonify(proyectos), status

@proyecto_bp.route('/crear', methods=['POST'])
@jwt_required()
def crear_proyecto():
    id_usuario = get_jwt_identity()
    datos = request.form.to_dict(flat=False)
    imagen = request.files.get('FOTO_PROYECTO')

    resultado, status = cargar_proyecto(id_usuario, datos, imagen)
    return jsonify(resultado), status





@proyecto_bp.route('/etiquetas', methods=['GET'])
@jwt_required()
def etiquetas():
    etiqueta, status = obtener_etiquetas()
    return jsonify(etiqueta), status
