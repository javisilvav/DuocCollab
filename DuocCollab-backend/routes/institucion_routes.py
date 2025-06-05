from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.institucion_services import (
    obtener_sedes, 
    obtener_escuelas, 
    obtener_carreras, 
    obtener_sede_escuela,
    cargar_escuela,
    actualizar_escuela,
    eliminar_escuela,
    cargar_carrera,
    actualizar_carrera,
    cargar_sede,
    actualizar_sede,
    cargar_sd_esc,
    actualizar_sd_esc,

)


institucion_bp = Blueprint('institucion_bp',__name__, url_prefix='/api/institucion')



@institucion_bp.route('/sede_escuela', methods=['GET'])
def sede_escuela():
    return jsonify(obtener_sede_escuela())


@institucion_bp.route('/crear_sd_esc', methods=['POST'])
@jwt_required()
def crear_sd_esc():
    datos = request.get_json()
    resultado, status = cargar_sd_esc(datos)
    return jsonify(resultado), status

@institucion_bp.route('/editar_sd_esc', methods=['POST'])
@jwt_required()
def editar_sd_esc():
    datos = request.get_json()
    resultado, status = actualizar_sd_esc(datos)
    return jsonify(resultado), status







@institucion_bp.route('/escuelas', methods=['GET'])
def escuelas():
    escuelas, status = obtener_escuelas()
    return jsonify(escuelas), status


@institucion_bp.route('/crear_escuela', methods=['POST'])
@jwt_required()
def crear_escuela():
    datos = request.get_json()
    resultado, status = cargar_escuela(datos)
    return jsonify(resultado), status

@institucion_bp.route('/editar_escuela', methods=['POST'])
@jwt_required()
def editar_escuela():
    datos = request.get_json()
    resultado, status = actualizar_escuela(datos)
    return jsonify(resultado), status


@institucion_bp.route('/eliminar_escuela', methods=['POST'])
@jwt_required()
def elimina_escuela():
    datos = request.get_json()
    resultado, status = eliminar_escuela(datos)
    return jsonify(resultado), status









@institucion_bp.route('/carreras', methods=['GET'])
def carreras():
    carreras, status =obtener_carreras()
    return jsonify(carreras), status

@institucion_bp.route('/crear_carrera', methods=['POST'])
@jwt_required()
def crear_carrera():
    datos = request.get_json()
    resultado, status = cargar_carrera(datos)
    return jsonify(resultado), status

@institucion_bp.route('/editar_carrera', methods=['POST'])
@jwt_required()
def editar_carrera():
    datos = request.get_json()
    resultado, status = actualizar_carrera(datos)
    return jsonify(resultado), status




@institucion_bp.route('/sedes', methods=['GET'])
def sedes():
    sedes, status = obtener_sedes()
    return jsonify(sedes), status

@institucion_bp.route('/crear_sede', methods=['POST'])
@jwt_required()
def crear_sede():
    datos = request.get_json()
    resultado, status = cargar_sede(datos)
    return jsonify(resultado), status

@institucion_bp.route('/editar_sede', methods=['POST'])
@jwt_required()
def editar_sede():
    datos = request.get_json()
    resultado, status = actualizar_sede(datos)
    return jsonify(resultado), status


