from flask import Blueprint, request, jsonify
from services.institucion_service import *
from .auth import verificar_token

institucion_bp = Blueprint('institucion', __name__)

# Sede
@institucion_bp.route('/api/sedes', methods=['GET','POST'])
def sedes():
    verificar_token()
    if request.method == 'GET': return jsonify(list_sedes())
    resp = add_sede(request.json)
    return (jsonify({'mensaje':'Sede creada'}),201) if resp.ok else (jsonify({'error':resp.text}),resp.status_code)

# Carrera
@institucion_bp.route('/api/carreras', methods=['GET','POST'])
def carreras():
    verificar_token()
    if request.method=='GET': return jsonify(list_carreras())
    resp=add_carrera(request.json)
    return (jsonify({'mensaje':'Carrera creada'}),201) if resp.ok else (jsonify({'error':resp.text}),resp.status_code)

# Escuela
@institucion_bp.route('/api/escuelas', methods=['GET','POST'])
def escuelas():
    verificar_token()
    if request.method=='GET': return jsonify(list_escuelas())
    resp=add_escuela(request.json)
    return (jsonify({'mensaje':'Escuela creada'}),201) if resp.ok else (jsonify({'error':resp.text}),resp.status_code)

# Sede-Escuela
@institucion_bp.route('/api/sedeEscuela', methods=['GET','POST'])
def sede_escuela():
    verificar_token()
    if request.method=='GET': return jsonify(list_sede_escuela())
    resp=add_sede_escuela(request.json)
    return (jsonify({'mensaje':'Vinculo creado'}),201) if resp.ok else (jsonify({'error':resp.text}),resp.status_code)