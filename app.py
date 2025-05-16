import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# importar Flask y crear una instancia del objeto Flask
from flask import Flask, render_template, request, redirect, url_for, send_file
from collections import Counter

import csv
import os

# librería estándar para trabajar con expresiones regulares (regular expressions).
#import re
# El módulo datetime maneja fechas y horas en Python
from datetime import datetime

app = Flask(__name__)

# use Flask app.route decorador para mapear la ruta URL / a esa función

@app.route('/', methods=["GET", "POST"])
def proyecto():
    archivo = os.path.join('data', 'datos_usuarios.csv')

    # Leer el archivo CSV y generar los datos del gráfico
    if os.path.isfile(archivo):
        df = pd.read_csv(archivo)
        resumen = df['Tarjeta'].value_counts()
        labels = resumen.index.tolist()
        data = resumen.values.tolist()
    else:
        labels = []
        data = []

    return render_template("sitio1.html", labels=labels, data=data)

# sub paginas

@app.route("/Servicios")
def sub2():
    return render_template("Servicios.html")

@app.route("/Promociones")
def sub3():
    return render_template("Promociones.html")


@app.route("/grafico_interactivo", methods=["GET", "POST"])
def grafico_interactivo():
    archivo = os.path.join('data', 'datos_usuarios.csv')

    # Si vienen datos del formulario, guardarlos en el CSV
    if request.method == 'POST':
        nombre = request.form['txtNombre']
        apellido = request.form['txtApellido']
        correo = request.form['miEmail']
        telefono = request.form['telefono']
        fecha = request.form['fecha']
        tarjeta = request.form['tarjeta']

        existe = os.path.isfile(archivo)

        with open(archivo, 'a', newline='', encoding='utf-8') as csvfile:
            campos = ['Nombre','Apellido', 'Correo', 'Teléfono', 'Fecha', 'Tarjeta']
            writer = csv.DictWriter(csvfile, fieldnames=campos)
            if not existe:
                writer.writeheader()
            writer.writerow({
                'Nombre': nombre,
                'Apellido': apellido,
                'Correo': correo,
                'Teléfono': telefono,
                'Fecha': fecha,
                'Tarjeta': tarjeta
            })

    # Leer el archivo CSV y generar los datos del gráfico
    if os.path.isfile(archivo):
        df = pd.read_csv(archivo)
        resumen = df['Tarjeta'].value_counts()
        labels = resumen.index.tolist()
        data = resumen.values.tolist()
    else:
        labels = []
        data = []

    return render_template("sitio1.html", labels=labels, data=data)


@app.route('/Productos')
def sub1():
    # Crear gráfico
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [10, 20, 25, 30], marker='o')
    ax.set_title('Ventas del Mes')
    ax.set_xlabel('Semana')
    ax.set_ylabel('Ventas')

    # Ruta correcta con carpeta 'imagenes'
    ruta_archivo = os.path.join(app.static_folder, 'imagenes', 'grafico_guardado.png')
    os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)  # Crear carpeta si no existe

    plt.close(fig)
    return render_template('Productos.html')
