from flask import Flask

def create_app():
    app = Flask(__name__)

    # Registrar las rutas desde routes.py
    with app.app_context():
        from .routes import app as routes_app
        app.register_blueprint(routes_app)

    return app