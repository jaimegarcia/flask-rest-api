from flask import Flask,request,jsonify,abort
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
    lista_estudiantes=[estudiantes_db[key] for key in estudiantes_db.keys()]
    return jsonify({"data":lista_estudiantes}),200

@app.route("/estudiantes/<int:id>",methods=['GET'])
def obtener_estudiante(id):
    try:
      estudiante=estudiantes_db[str(id)]
      return jsonify(estudiante),200
    except:
      error_message={"error":f"No se encontró ningún estudiante con el ID {id}"}
      return jsonify(error_message),400


@app.route("/estudiantes",methods=['POST'])
def agregar_estudiante():

  estudiante_id=str(request.json["cedula"])
  if(estudiante_id in estudiantes_db):
    error_message={"error":f"Ya existe un estudiante registrando con el ID {estudiante_id}"}
    return jsonify(error_message),400
    
  try:  
    nuevo_estudiante=dict()
    nuevo_estudiante["cedula"]=request.json["cedula"]
    nuevo_estudiante["nombre"]=request.json["nombre"]
    nuevo_estudiante["apellido"]=request.json["apellido"]
    nuevo_estudiante["carrera"]=request.json["carrera"]
    nuevo_estudiante["correo"]=request.json["correo"]
    estudiantes_db[estudiante_id]=nuevo_estudiante
    return jsonify(nuevo_estudiante),201
  except:
      error_message={"error":"Los datos del estudiante no están completos o son incorrectos"}
      return jsonify(error_message),400

@app.route("/estudiantes/<int:id>",methods=['PUT'])
def actualizar_estudiante(id):

  try:
    estudiante_id=str(id)
    estudiante=estudiantes_db[estudiante_id]
  except:
    error_message={"error":f"No se encontró ningún estudiante con el ID {id}"}
    return jsonify(error_message),400
  try:
    estudiante["cedula"]=request.json["cedula"]
    estudiante["nombre"]=request.json["nombre"]
    estudiante["apellido"]=request.json["apellido"]
    estudiante["carrera"]=request.json["carrera"]
    estudiante["correo"]=request.json["correo"]
    estudiantes_db[estudiante_id]=estudiante
    return jsonify(estudiante),200
  except:
    error_message={"error":"Los datos del estudiante no están completos o son incorrectos"}
    return jsonify(error_message),400

@app.route("/estudiantes/<int:id>",methods=['DELETE'])
def eliminar_estudiante(id):
  try:
    estudiante_id=str(id)
    del estudiantes_db[estudiante_id]
    result={"cedula":id,"borrado":True}
    return jsonify(result),200
  except:
    error_message={"error":f"No se encontró ningún estudiante con el ID {id}"}
    return jsonify(error_message),400

if __name__ == '__main__':
    app.run(debug=True)