from flask import Flask
from routes.usuario_routes import usuario_bp
from routes.institucion_routes import institucion_bp
from routes.proyecto_routes import proyecto_bp

app = Flask(__name__)

app.register_blueprint(usuario_bp)
app.register_blueprint(institucion_bp)
app.register_blueprint(proyecto_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)