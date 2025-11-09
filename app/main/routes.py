from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from .. import db
from ..models import Producto

main_bp = Blueprint("main", __name__)


def get_carrito():
    return session.setdefault("carrito", {})


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/panel")
def panel():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para acceder al panel.", "warning")
        return redirect(url_for("auth.login"))

    return render_template("panel.html", nombre=session.get("usuario_nombre"))


@main_bp.route("/productos", methods=["GET", "POST"])
def productos():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para gestionar productos.", "warning")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        nombre = request.form.get("nombre")
        precio = request.form.get("precio")
        descripcion = request.form.get("descripcion")

        if not nombre or not precio:
            flash("Nombre y precio son obligatorios.", "danger")
        else:
            try:
                precio = float(precio)
            except ValueError:
                flash("El precio debe ser numérico.", "danger")
            else:
                nuevo = Producto(
                    nombre=nombre,
                    precio=precio,
                    descripcion=descripcion,
                    usuario_id=session.get("usuario_id"),
                )
                db.session.add(nuevo)
                db.session.commit()
                flash("Producto creado correctamente.", "success")
                return redirect(url_for("main.productos"))

    productos = Producto.query.order_by(Producto.creado_en.desc()).all()
    return render_template("productos.html", productos=productos)


@main_bp.route("/productos/<int:producto_id>/editar", methods=["GET", "POST"])
def editar_producto(producto_id):
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para editar productos.", "warning")
        return redirect(url_for("auth.login"))

    producto = Producto.query.get_or_404(producto_id)

    if request.method == "POST":
        nombre = request.form.get("nombre")
        precio = request.form.get("precio")
        descripcion = request.form.get("descripcion")

        if not nombre or not precio:
            flash("Nombre y precio son obligatorios.", "danger")
        else:
            try:
                precio = float(precio)
            except ValueError:
                flash("El precio debe ser numérico.", "danger")
            else:
                producto.nombre = nombre
                producto.precio = precio
                producto.descripcion = descripcion
                db.session.commit()
                flash("Producto actualizado correctamente.", "success")
                return redirect(url_for("main.productos"))

    return render_template("editar_producto.html", producto=producto)


@main_bp.route("/productos/<int:producto_id>/eliminar")
def eliminar_producto(producto_id):
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para eliminar productos.", "warning")
        return redirect(url_for("auth.login"))

    producto = Producto.query.get_or_404(producto_id)
    db.session.delete(producto)
    db.session.commit()
    flash("Producto eliminado correctamente.", "info")
    return redirect(url_for("main.productos"))


@main_bp.route("/carrito/agregar/<int:producto_id>")
def agregar_carrito(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    carrito = get_carrito()
    pid = str(producto.id)
    carrito[pid] = carrito.get(pid, 0) + 1
    session["carrito"] = carrito
    flash(f"Se agregó {producto.nombre} al carrito.", "success")
    return redirect(url_for("main.productos"))


@main_bp.route("/carrito")
def carrito():
    carrito = get_carrito()
    productos = []
    total = 0.0

    if carrito:
        ids = [int(pid) for pid in carrito.keys()]
        productos_db = Producto.query.filter(Producto.id.in_(ids)).all()
        productos_map = {p.id: p for p in productos_db}

        for pid_str, cantidad in carrito.items():
            pid = int(pid_str)
            p = productos_map.get(pid)
            if p:
                subtotal = p.precio * cantidad
                total += subtotal
                productos.append(
                    {
                        "id": p.id,
                        "nombre": p.nombre,
                        "precio": p.precio,
                        "cantidad": cantidad,
                        "subtotal": subtotal,
                    }
                )

    return render_template("carrito.html", productos=productos, total=total)


@main_bp.route("/carrito/vaciar")
def vaciar_carrito():
    session["carrito"] = {}
    flash("Carrito vaciado.", "info")
    return redirect(url_for("main.carrito"))
