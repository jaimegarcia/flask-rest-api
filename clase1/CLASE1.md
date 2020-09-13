# flask-rest-api



pip freeze > requirements.txt

git config user.name "nombredeusuario"
git config user.email "email"

python3 -m venv env

Flask==1.1.2


pip3 install -r requirements.txt


from flask import Flask
app = Flask(__name__)


@app.route("/")
def hola_mundo():
  return "Hola, Mundo!"


# flask depende de esta variable de entorno para encontrar el archivo principal
export FLASK_APP=app.py

# Ahora solo debemos decirle a flask que corra
flask run

# * Serving Flask app "app.py"
# * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)


# Para que la aplicacion se recargue de forma automatica con cada cambio
export FLASK_DEBUG=1

# Cambiemos algo del codigo

from flask import Flask
app = Flask(__name__)


@app.route("/")
def hola_mundo():
  return "Adios, Mundo!"


# Agreguemos una nueva ruta pero con un parametro



@app.route("/saludo/<nombre>")
def saludo(nombre):
  return f"Hola {nombre}"



@app.route("/saludo/<string:nombre>")
def saludo(nombre):
  return f"Hola {nombre}"


@app.route("/saludo/<string:nombre>")
def saludo(nombre):
  titulo = request.args.get('titulo', '')
  return f"Hola {titulo} {nombre}"

http://localhost:5000/saludo/jaime?titulo=Mr


@app.route("/estudiantes/<int:id>/notas")
def notas(id):
  notas=[4,3,2,1,3]
  return f"Las notas del (la) estudiante con ID {id} son {notas}"



@app.route("/estudiantes/<int:id>/notas")
def notas(id):
  notas={
  "11234224":[4,3,2,1,2],
  "12434236":[5,3,5,5,5],
  "61236224":[1,3,2,1,1],
  "52433236":[3,3,3,3,3]
  }
  notas_estudiante=notas[str(id)]
  return f"Las notas del (la) estudiante con ID {id} son {(notas_estudiante)}"


# Agregamos ruta


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


@app.route("/estudiantes/<int:id>")
def estudiantes(id):
  print("estudiante",estudiantesDB[str(id)])
  nombre_estudiante=estudiantesDB[str(id)]['nombre']
  return f"La estudiante con ID {id} se llama {nombre_estudiante}"

@app.route("/estudiantes/<int:id>/notas")
def notas(id):

  notas_estudiante=estudiantesDB[str(id)]['notas']
  return f"Las notas del (la) estudiante con ID {id} son {(notas_estudiante)}"


# Agregamos formato
@app.route("/estudiantes/<int:id>/notas")
def notas(id):

  notas_estudiante=estudiantesDB[str(id)]['notas']
  notas_estudiante_str=", ".join(map(str, notas_estudiante))
  return f"Las notas del (la) estudiante con ID {id} son {notas_estudiante_str}"


# Agregamos una consulta


@app.route("/estudiantes")
def estudiantes_lista():
  lista_estudiantes=[]
  for estudiante in estudiantesDB.keys():
    lista_estudiantes.append(estudiantesDB[estudiante]["nombre"])

  return f"Los estudiantes de este curso son {lista_estudiantes}"


REST

REpresentational State Transfer*
- Concepts include:
• Separation of Client and Server
• Server Requests are Stateless
• Cacheable Requests
• Uniform Interface


Use pronombres en plural para indicar los recursos asociados

estudiantes


estudiantes/1324345

El identificador a la derecha del recurso indica que se va a realizar operaciones con el Estudiante con ID  1324345

estudiantes/1324345/tareas

Si el recurso tiene asociado

/v1/estudiantes/1324345/tareas/12

Utilice los query strings para propiedades no asociadas a los recurso

/estudiantes?ordenar=nombre
/estudiantes?pagina=1
/estudiantes?formato=json


string

(default) accepts any text without a slash

int

accepts positive integers

float

accepts positive floating point values

path

like string but also accepts slashes

uuid

accepts UUID strings



Utilice los verbos de HTTP siempre que sea posible

GET
- Obtiene un recurso
POST
- Agrega un nuevo recurso 
PUT
- Actualiza un recurso existente
PATCH
- Actualiza de forma parcial un recurso existente
DELETE
- Borra un recurso existente


POST /estudiantes/1324345/tareas/12/aprobar


| Recurso  | GET | POST | PUT | DELETE |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| /estudiantes  | Obtener Lista  | Crear elemento  | Actualizar Batch  | Error |
| /estudiantes/1324345  | Obtener Elemento  | Error  | Actualizar Elemento  | Borrar Elemento |


Idempotencia: Operación que puede ser aplica múltiples veces, sin cambiar el resultado

- GET, PUT, PATCH y DELETE: Idempotentes
- POST no es idempotente


Diseñando resultados


Sea consistente (snake_case, camelCase, spinal-case)
No expongan datos de servidor
No exponga datos privados
No exponga datos que puedan generar brechas de seguridad