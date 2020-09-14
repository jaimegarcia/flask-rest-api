from flask import Flask,request
import sys

app = Flask(__name__)


estudiantes_db={
  "11234224":{
    "cedula":11234224,
    "nombre":"Juana",
    "apellido":"Correa",
    "correo":"juana.correa@misena.edu.co",
    "carrera":"Electrónica"
  },
  "12434236":{
    "cedula":12434236,
    "nombre":"Jaime",
    "apellido":"García",
    "correo":"jaime.garcia@misena.edu.co",
    "carrera":"Administración"
  },
  "61236224":{
    "cedula":61236224,
    "nombre":"Roberta",
    "apellido":"Mejia",
    "correo":"roberta.mejia@misena.edu.co",
    "carrera":"Sistemas"
  },
  "52433236":{
    "cedula":52433236,
    "nombre":"Miriam",
    "apellido":"Zapata",
    "correo":"miriam.zapata@misena.edu.co",
    "carrera":"Sistemas"
  }
}


@app.route("/")
def hola_mundo():
  print("holas")
  return "Adiós, Mundo!"


@app.route("/saludo/<string:nombre>")
def saludo(nombre):
  titulo = request.args.get('titulo', '')
  return f"Hola {titulo} {nombre}"


@app.route("/estudiantes",methods=['GET'])
def obtener_estudiantes():
    lista_estudiantes=[f"{estudiantes_db[key]['nombre']} {estudiantes_db[key]['apellido']}" for key in estudiantes_db.keys()]
    return f"Los estudiantes de este curso son {', '.join(lista_estudiantes)}"

@app.route("/estudiantes/<int:id>",methods=['GET'])
def obtener_estudiante(id):
    estudiante=estudiantes_db[str(id)]
    return f"Estudiante con cédula {id} se llama {estudiante['nombre']} {estudiante['apellido']} y es de la carrera {estudiante['carrera']} "


@app.route("/estudiantes",methods=['POST'])
def agregar_estudiante():
    estudiante_id=str(request.json["cedula"])
    estudiantes_db[estudiante_id]=request.json
    return f"Estudiante con ID {estudiante_id} agregado"

@app.route("/estudiantes/<int:id>",methods=['PUT'])
def actualizar_estudiante(id):
    estudiante_id=str(id)
    estudiantes_db[estudiante_id]=request.json
    print(estudiantes_db)
    return f"Estudiante con ID {estudiante_id} actualizado"

@app.route("/estudiantes/<int:id>",methods=['DELETE'])
def eliminar_estudiante(id):
    estudiante_id=str(id)
    del estudiantes_db[estudiante_id]
    print(estudiantes_db)
    return f"Estudiante con ID {estudiante_id} eliminado"

if __name__ == '__main__':
    app.run(debug=True)