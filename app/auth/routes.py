from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from .. import db
from ..models import Usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")
        password = request.form.get("password")

        if not nombre or not correo or not password:
            flash("Todos los campos son obligatorios.", "danger")
            return render_template("registro.html")

        existente = Usuario.query.filter_by(correo=correo).first()
        if existente:
            flash("Ya existe un usuario con ese correo.", "warning")
            return render_template("registro.html")

        hash_pass = generate_password_hash(password)
        nuevo = Usuario(nombre=nombre, correo=correo, password=hash_pass)
        db.session.add(nuevo)
        db.session.commit()
        flash("Usuario registrado correctamente. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("auth.login"))

    return render_template("registro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form.get("correo")
        password = request.form.get("password")

        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and check_password_hash(usuario.password, password):
            session["usuario_id"] = usuario.id
            session["usuario_nombre"] = usuario.nombre
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for("main.panel"))
        else:
            flash("Correo o contraseña incorrectos.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("main.index"))
