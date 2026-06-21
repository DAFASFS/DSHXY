from flask import Flask, render_template, redirect, url_for
import socket

app = Flask(__name__)

HOST = "192.168.100.21"   # IP del servidor
PORT = 12345              # Puerto del servidor

NOMBRE = "Daniel Constanso"


def leer_sensor():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            s.connect((HOST, PORT))

            data = s.recv(1024).decode().strip()
            print("RECIBIDO:", data)

            ejeX, ejeY = data.split(',')

            ejeX = float(ejeX.replace('X:', '').strip())
            ejeY = float(ejeY.replace('Y:', '').strip())

            return ejeX, ejeY

    except Exception as e:
        print("ERROR:", e)
        return 0, 0


def normalizar(valor):
    valor = abs(float(valor))
    valor = round(valor)

    if valor < 1:
        valor = 1

    if valor > 5:
        valor = 5

    return int(valor)


def mostrar_pagina(color, color_css):
    sensorX, sensorY = leer_sensor()

    # Se mantiene el orden que tenías en tu código original:
    # ejeY, ejeX = leer_sensor()
    ejeX = normalizar(sensorY)
    ejeY = normalizar(sensorX)

    return render_template(
        "index.html",
        ejeX=ejeX,
        ejeY=ejeY,
        color=color,
        color_css=color_css,
        nombre=NOMBRE
    )


@app.route("/")
def index():
    return redirect(url_for("pagina_verde"))


@app.route("/verde")
def pagina_verde():
    return mostrar_pagina("Verde", "green")


@app.route("/rojo")
def pagina_rojo():
    return mostrar_pagina("Rojo", "red")


@app.route("/azul")
def pagina_azul():
    return mostrar_pagina("Azul", "blue")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
