import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
from collections import Counter
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuración base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    correo = db.Column(db.String(100))
    telefono = db.Column(db.String(50))
    fecha = db.Column(db.String(20))
    tarjeta = db.Column(db.String(50))

# Crear base de datos (ejecutar solo una vez)
with app.app_context():
    if not os.path.exists('data'):
        os.makedirs('data')
    db.create_all()

@app.route('/', methods=["GET"])
def proyecto():
    # Mostrar resumen de tarjetas
    usuarios = Usuario.query.all()
    tarjetas = [u.tarjeta for u in usuarios]
    resumen = Counter(tarjetas)
    labels = list(resumen.keys())
    data = list(resumen.values())

    return render_template("sitio1.html", labels=labels, data=data)

# Páginas secundarias
@app.route("/Servicios")
def sub2():
    return render_template("Servicios.html")

@app.route("/Promociones")
def sub3():
    return render_template("Promociones.html")

@app.route("/grafico_interactivo", methods=["GET", "POST"])
def grafico_interactivo():
    if request.method == 'POST':
        nuevo_usuario = Usuario(
            nombre=request.form['txtNombre'],
            apellido=request.form['txtApellido'],
            correo=request.form['miEmail'],
            telefono=request.form['telefono'],
            fecha=request.form['fecha'],
            tarjeta=request.form['tarjeta']
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

    usuarios = Usuario.query.all()
    tarjetas = [u.tarjeta for u in usuarios]
    resumen = Counter(tarjetas)
    labels = list(resumen.keys())
    data = list(resumen.values())

    return render_template("sitio1.html", labels=labels, data=data)

@app.route('/Productos')
def sub1():
    # Crear gráfico (ejemplo estático)
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [10, 20, 25, 30], marker='o')
    ax.set_title('Ventas del Mes')
    ax.set_xlabel('Semana')
    ax.set_ylabel('Ventas')

    plt.close(fig)
    return render_template('Productos.html')

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/ver_usuarios')
def ver_usuarios():
    usuarios = Usuario.query.all()  # Trae todos los usuarios
    return render_template('ver_usuarios.html', usuarios=usuarios)

