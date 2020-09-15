from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import pytz
from datetime import datetime

timezone = pytz.timezone("America/Bogota")

from models import Estudiante,Peticion

app = Flask(__name__)

# Inicializar Firestore DB
cred = credentials.Certificate('key/key.json')
default_app = initialize_app(cred)
db = firestore.client()
estudiantes_ref = db.collection('Estudiantes')
peticiones_ref = db.collection('Peticiones')


nuevo_estudiante=Estudiante(122345, "Jaime", "Garcia", "jaime.garcia", "Electronica")
print(nuevo_estudiante.to_dict())

nueva_fecha_creacion=timezone.localize(datetime.now())
nueva_fecha_atencion=timezone.localize(datetime.strptime('25/09/20 7:00:00', '%d/%m/%y %H:%M:%S'))

nueva_peticion=Peticion(122345, "Asesoria",nueva_fecha_creacion,nueva_fecha_atencion)
print(nueva_peticion.to_dict(),nueva_peticion.fecha_creacion,nueva_peticion.fecha_atencion)




@app.route("/api/estudiantes",methods=['POST'])
def agregar_estudiante():

    data=request.json
    estudiante_id=str(request.json["cedula"])
    estudiante_doc=estudiantes_ref.document(estudiante_id)
    if(estudiante_doc.get().exists):
        error_message={"error":f"Ya existe un estudiante registrando con el ID {estudiante_id}"}
        return jsonify(error_message),400
    try:  
        nuevo_estudiante=Estudiante(data["cedula"], data["nombre"], data["apellido"],data["correo"], data["carrera"]).to_dict()
        estudiante_doc.set(nuevo_estudiante)
        return jsonify(nuevo_estudiante),201
    except:
        error_message={"error":"Los datos del estudiante no están completos o son incorrectos"}
        return jsonify(error_message),400


@app.route("/api/estudiantes/<int:id>",methods=['GET'])
def obtener_estudiante(id):

    estudiante_doc=estudiantes_ref.document(str(id)).get()
    if(estudiante_doc.exists):
      print("estudiante_doc",estudiante_doc.to_dict())
      return jsonify(estudiante_doc),200
    else:
      error_message={"error":f"No se encontró ningún estudiante con el ID {id}"}
      return jsonify(error_message),400


@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    print("create")
    try:
        id = request.json['id']
        print("request",request)
        estudiantes_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON.
        todo : Return document that matches query ID.
        all_todos : Return all documents.
    """
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')
        if todo_id:
            todo = estudiantes_ref.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in estudiantes_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/update/<id>', methods=['POST', 'PUT'])
def update(id):
    """
        update() : Update document in Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        estudiantes_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


if __name__ == '__main__':
    app.run(debug=True)