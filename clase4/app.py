from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app


from models import Estudiante,Peticion

def to_dict_with_id(item):
    """Convierte documentos de Cloud Firestore a Diccionarios con id

    Argumentos:
        item (class): Documento de Cloud Firestore 

    Retorna:
        dict: Diccionario con id del documento
    """
    print(item,item.id)
    item_dict=item.to_dict()
    item_dict["id"]=item.id
    return item_dict

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




@app.route("/api/v1/estudiantes",methods=['POST'])
def agregar_estudiante():
    """Agrega un estudiante a la base de datos

    Retorna:
        json: Objeto con los datos del estudiante agregado o error si falló el proceso
    """
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

@app.route("/api/v1/estudiantes",methods=['GET'])
def obtener_lista_estudiantes():
    """Obtiene la lista de estudiantes de la base de datos
    
    Retorna:
        json: Objeto con la lista de estudiantes o error si falló el proceso
    """
    results=estudiantes_ref.stream()
    lista_estudiantes=[item.to_dict() for item in results]

    return jsonify({"data":lista_estudiantes}),200

@app.route("/api/v1/estudiantes/<int:id>",methods=['GET'])
def obtener_estudiante(id):
    """Obtiene un estudiante de la base de datos a partir del id
    
    Argumentos:
        id (int): Id con la cédula del estudiante
    Retorna:
        json: Objeto con la información del estudiante o error si falló el proceso
    """
    estudiante_doc=estudiantes_ref.document(str(id)).get()
    if(estudiante_doc.exists):
      return jsonify(estudiante_doc.to_dict()),200
    else:
      error_message={"error":f"No se encontró ningún estudiante con el ID {id}"}
      return jsonify(error_message),400


@app.route("/api/v1/estudiantes/<int:id>",methods=['PUT'])
def actualizar_estudiante(id):
    """Actualiza un estudiante de la base de datos a partir del id
    
    Argumentos:
        id (int): Id con la cédula del estudiante
    Retorna:
        json: Objeto con la información del estudiante actualizada o error si falló el proceso
    """
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


@app.route("/api/v1/estudiantes/<int:id>",methods=['DELETE'])
def eliminar_estudiante(id):
    """Elimina un estudiante de la base de datos a partir del id
    
    Argumentos:
        id (int): Id con la cédula del estudiante
    Retorna:
        json: Objeto con la cedula del estudiante borrado o error si falló el proceso
    """
    estudiante_id=str(id)
    estudiante_doc=estudiantes_ref.document(estudiante_id)

    if(estudiante_doc.get().exists):
        estudiante_doc.delete()
        result={"cedula":id,"borrado":True}
        return jsonify(result),200
    else:
        error_message={"error":f"No se encontró ningún estudiante con el ID {id}"}
        return jsonify(error_message),400



@app.route("/api/v1/estudiantes/<int:id>/peticiones",methods=['POST'])
def crear_peticion(id):
    """Crea una petición de la base de datos a partir del id del estudiante
    
    Argumentos:
        id (int): Id con la cédula del estudiante
    Retorna:
        json: Objeto con la petición del estudiante creada o error si falló el proceso
    """
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


@app.route("/api/v1/estudiantes/<int:id>/peticiones",methods=['GET'])
def obtener_peticiones(id):
    """Obtiene la lista de peticiones de un estudiante de la base de datos a partir del id del estudiante
    
    Argumentos:
        id (int): Id con la cédula del estudiante
    Retorna:
        json: Objeto con la lista de peticiones del estudiante creada o error si falló el proceso
    """
    estudiante_id=str(id)
    estudiante_doc=estudiantes_ref.document(estudiante_id)

    if(estudiante_doc.get().exists):
        try:  
            query = peticiones_ref.where('cedula','==',id).order_by('fecha_atencion')
            results = query.stream()
            lista_peticiones=[to_dict_with_id(item) for item in results]
            return jsonify({"data":lista_peticiones}),200
        except Exception as err:
            error_message={"error":"Los datos de la petición no están completos o son incorrectos"}
            return jsonify(error_message),400
    else:
        error_message={"error":f"No se encontró ningún estudiante con el ID {id}"}
        return jsonify(error_message),400


@app.route("/api/v1/estudiantes/<int:id>/peticiones/<string:pid>",methods=['GET','PATCH','PUT','DELETE'])
def procesar_peticion(id,pid):
    """Obtiene, Actualiza parcial o totalmente, o Elimina una Petición a partir del ID de la petición y la cédula del estudiante
    
    Argumentos:
        id (int): Id con la cédula del estudiante
        pid (str): Id de la petición
    Retorna:
        json: Objeto con la petición del estudiante procesada o error si falló el proceso
    """
    estudiante_id=str(id)
    estudiante_doc=estudiantes_ref.document(estudiante_id).get()

    if(estudiante_doc.exists):
        peticion_doc = peticiones_ref.document(pid).get()
        if(peticion_doc.exists): 
            if(request.method=='GET'):
                peticion_dict=peticion_doc.to_dict()
                peticion_dict["id"]=pid
                return jsonify(peticion_dict),200
            elif(request.method=='PATCH'):
                data=request.json
                try:  
                    nuevo_estado=data["estado"]
                    peticiones_ref.document(pid).update({"estado":nuevo_estado})
                    peticion_dict=peticion_doc.to_dict()
                    peticion_dict["id"]=pid
                    peticion_dict["estado"]=nuevo_estado
                    return jsonify(peticion_dict),200
                except Exception as err:
                    error_message={"error":"Los datos de la petición no están completos o son incorrectos"}
                    return jsonify(error_message),400
            elif(request.method=='PUT'):
                data=request.json
                try:  
                    nueva_peticion=Peticion(data["cedula"], data["peticion"], data["fecha_atencion"],data["estado"]).to_dict()
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