from flask import request, abort
from config import API_TOKEN

def verificar_token():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        abort(401, description="Token inválido o faltante")

    token = auth_header.split(" ")[1]
    if token != API_TOKEN:
        abort(403, description="Token no autorizado")
