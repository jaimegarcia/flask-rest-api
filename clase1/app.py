from flask import Flask,request
app = Flask(__name__)

estudiantesDB={
  "11234224":{
    "nombre":"Juana Correa",
    "notas":[4,3,2,1,2]
  },
  "12434236":{
    "nombre":"Jaime García",
    "notas":[5,3,5,5,5]
  },
  "61236224":{
    "nombre":"Roberta Mejía",
    "notas":[1,3,2,1,1]
  },
  "52433236":{
    "nombre":"Miriam Zapata",
    "notas":[3,3,3,3,3]
  }
}


@app.route("/")
def hola_mundo():
  return "Adiós, Mundo!"


@app.route("/saludo/<string:nombre>")
def saludo(nombre):
  titulo = request.args.get('titulo', '')
  return f"Hola {titulo} {nombre}"


@app.route("/estudiantes")
def estudiantes_lista():
  lista_estudiantes=[]
  for estudiante in estudiantesDB.keys():
    lista_estudiantes.append(estudiantesDB[estudiante]["nombre"])

  return f"Los estudiantes de este curso son {lista_estudiantes}"

@app.route("/estudiantes/<int:id>")
def estudiantes(id):
  nombre_estudiante=estudiantesDB[str(id)]['nombre']
  return f"La estudiante con ID {id} se llama {nombre_estudiante}"

@app.route("/estudiantes/<int:id>/notas")
def notas(id):

  notas_estudiante=estudiantesDB[str(id)]['notas']
  notas_estudiante_str=", ".join(map(str, notas_estudiante))
  return f"Las notas del (la) estudiante con ID {id} son {notas_estudiante_str}"