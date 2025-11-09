from . import db
from datetime import datetime


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    productos = db.relationship("Producto", backref="creador", lazy=True)

    def __repr__(self):
        return f"<Usuario {self.nombre}>"


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(250))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))

    def __repr__(self):
        return f"<Producto {self.nombre} - {self.precio}>"
