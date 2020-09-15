from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app


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



nueva_peticion=Peticion(122345, "Asesoria",'25/09/20 7:00:00')
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

@app.route("/api/estudiantes/",methods=['GET'])
def obtener_lista_estudiantes(id):

    results=estudiantes_ref.document(str(id)).stream()
    lista_estudiantes=[item for item in results]

    return jsonify({"data":lista_estudiantes}),200

@app.route("/api/estudiantes/<int:id>",methods=['GET'])
def obtener_estudiante(id):

    estudiante_doc=estudiantes_ref.document(str(id)).get()
    if(estudiante_doc.exists):
      print("estudiante_doc",estudiante_doc.to_dict())
      return jsonify(estudiante_doc),200
    else:
      error_message={"error":f"No se encontró ningún estudiante con el ID {id}"}
      return jsonify(error_message),400


@app.route("/api/estudiantes/<int:id>",methods=['PUT'])
def actualizar_estudiante(id):

    data=request.json
    estudiante_id=str(id)
    estudiante_doc=estudiantes_ref.document(estudiante_id)

    if(estudiante_doc.get().exists):
        try:  
            nuevo_estudiante=Estudiante(data["cedula"], data["nombre"], data["apellido"],data["correo"], data["carrera"]).to_dict()
            estudiantes_ref.document(estudiante_id).update(nuevo_estudiante)
            return jsonify(nuevo_estudiante),200
        except:
            error_message={"error":"Los datos del estudiante no están completos o son incorrectos"}
            return jsonify(error_message),400
    else:
        error_message={"error":f"No se encontró ningún estudiante con el ID {id}"}
        return jsonify(error_message),400


@app.route("/api/estudiantes/<int:id>",methods=['DELETE'])
def eliminar_estudiante(id):

    estudiante_id=str(id)
    estudiante_doc=estudiantes_ref.document(estudiante_id)

    if(estudiante_doc.get().exists):
        estudiante_doc.delete()
        result={"cedula":id,"borrado":True}
        return jsonify(result),200
    else:
        error_message={"error":f"No se encontró ningún estudiante con el ID {id}"}
        return jsonify(error_message),400



@app.route("/api/estudiantes/<int:id>/peticiones",methods=['POST'])
def crear_peticion(id):

    data=request.json
    estudiante_id=str(id)
    estudiante_doc=estudiantes_ref.document(estudiante_id)

    if(estudiante_doc.get().exists):
        try:  
            nueva_peticion=Peticion(data["cedula"], data["peticion"], data["fecha_atencion"]).to_dict()
            peticion_ref=peticiones_ref.add(nueva_peticion)
            nueva_peticion["id"]=peticion_ref[1].id

            return jsonify(nueva_peticion),200
        except:
            error_message={"error":"Los datos de la petición no están completos o son incorrectos"}
            return jsonify(error_message),400
    else:
        error_message={"error":f"No se encontró ningún estudiante con el ID {id}"}
        return jsonify(error_message),400


def to_dict_with_id(item):
    print(item,item.id)
    item_dict=item.to_dict()
    item_dict["id"]=item.id
    return item_dict

@app.route("/api/estudiantes/<int:id>/peticiones",methods=['GET'])
def obtener_peticiones(id):

    estudiante_id=str(id)
    estudiante_doc=estudiantes_ref.document(estudiante_id)

    if(estudiante_doc.get().exists):
        try:  
            query = peticiones_ref.where('cedula','==',id).order_by('fecha_atencion')
            results = query.stream()
            print("results",results)
            lista_peticiones=[to_dict_with_id(item) for item in results]
            print("lista_peticiones",lista_peticiones)

            return jsonify({"data":lista_peticiones}),200
        except Exception as err:
            print("err",err)
            error_message={"error":"Los datos de la petición no están completos o son incorrectos"}
            return jsonify(error_message),400
    else:
        error_message={"error":f"No se encontró ningún estudiante con el ID {id}"}
        return jsonify(error_message),400


@app.route("/api/estudiantes/<int:id>/peticiones/<string:pid>",methods=['GET','PUT','DELETE'])
def obtener_peticion(id,pid):

    estudiante_id=str(id)
    estudiante_doc=estudiantes_ref.document(estudiante_id).get()

    if(estudiante_doc.exists):
        peticion_doc = peticiones_ref.document(pid).get()
        if(peticion_doc.exists): 
            if(request.method=='GET'):
                peticion_dict=peticion_doc.to_dict()
                peticion_dict["id"]=pid
                return jsonify(peticion_dict),200
            elif(request.method=='PUT'):
                data=request.json
                try:  
                    nueva_peticion=Peticion(data["cedula"], data["peticion"], data["fecha_atencion"]).to_dict()
                    peticiones_ref.document(pid).update(nueva_peticion)
                    nueva_peticion["id"]=pid
                    return jsonify(nueva_peticion),200
                except:
                    error_message={"error":"Los datos de la petición no están completos o son incorrectos"}
                    return jsonify(error_message),400
            else:
                peticiones_ref.document(pid).delete()
                result={"peticion":pid,"borrado":True}
                return jsonify(result),200
        else:
            error_message={"error":f"No se encontró ninguna petición con el ID {pid}"}
            return jsonify(error_message),400
    else:
        error_message={"error":f"No se encontró ningún estudiante con el ID {id}"}
        return jsonify(error_message),400



if __name__ == '__main__':
    app.run(debug=True)