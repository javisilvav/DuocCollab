from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required,  get_jwt_identity

protected_bp = Blueprint('protected_bp',__name__, url_prefix='/api/protected')

@protected_bp.route('/perfil', methods=['GET'])
@jwt_required()
def perfil_usuario():
    user_id = get_jwt_identity()
    return jsonify({
        'mensaje':'Acceso autorizado',
        'usuario_id':user_id
    })