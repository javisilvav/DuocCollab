from flask import request, abort
import jwt
from config import SECRET_KEY

def generar_token(id_usuario):
    payload = {"id_usuario": id_usuario}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verificar_token():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        abort(401, description="Token no proporcionado")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        id_usuario = payload["id_usuario"]
        request.id_usuario = id_usuario
        return id_usuario
    except jwt.ExpiredSignatureError:
        abort(401, description="Token expirado")
    except jwt.InvalidTokenError:
        abort(403, description="Token inválido")
