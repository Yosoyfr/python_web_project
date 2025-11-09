from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "cambia-esta-clave-en-produccion"

    db.init_app(app)

    # Import models para que SQLAlchemy las conozca
    from . import models  # noqa: F401

    # Registrar blueprints
    from .auth.routes import auth_bp
    from .main.routes import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # Crear tablas si no existen
    with app.app_context():
        db.create_all()

    return app
