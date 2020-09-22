from flask import Flask,request,jsonify,abort
import sys

app = Flask(__name__)


@app.route("/")
def hola_mundo():
  print("holas")
  return "Adiós, Mundo!"


@app.route("/saludo/<string:nombre>")
def saludo(nombre):
  titulo = request.args.get('titulo', '')
  return f"Hola {titulo} {nombre}"


if __name__ == '__main__':
    app.run(debug=True)