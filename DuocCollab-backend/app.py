from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from routes.auth_routes import auth_bp
from routes.protected_routes import protected_bp
from routes.institucion_routes import institucion_bp
from routes.proyecto_routes import proyecto_bp

app = Flask(__name__)
app.config.from_object(Config)

jwt= JWTManager(app)
app.register_blueprint(auth_bp)
app.register_blueprint(protected_bp)
app.register_blueprint(institucion_bp)
app.register_blueprint(proyecto_bp)

if __name__ == '__main__':
    app.run(port=5050, debug=True)