# Módulo 3 Introducción a las arquitecturas y desarrollo con API Rest 
# Clase 2 

# Tabla de Contenido

<!-- toc -->

- [Conexión a la Base de Datos Cloud FireStore](#conexión-a-la-base-de-datos-cloud-firestore)
- [Creación de Clases con Modelo de Datos](#creación-de-clases-con-modelo-de-datos)
- [Creación de Rutas para Estudiantes](#creación-de-rutas-para-estudiantes)
  - [Agregar Estudiantes](#agregar-estudiantes)
  - [Obtener Estudiantes](#obtener-estudiantes)
  - [Actualizar y Borrar Estudiantes](#actualizar-y-borrar-estudiantes)


<!-- tocstop -->


## Conexión a la Base de Datos Cloud FireStore

Vamos a incluir dos librerías en nuestro requirements.txt: firebase-admin para la conexión con bases de datos y pytz para el manejo de zonas horarias

```python
Flask==1.1.2
firebase-admin==4.3.0
pytz==2020.1
```
Debemos tener activo el entorno virtual, si no lo tenemos- Hacemos click en Terminal y ejecutamos los siguientes comandos:

```bash
.venv\Scripts\activate
```

![python-15](images/python-15.png)

Si se genera el mensaje "Activate.ps1 is not digitally signed. You cannot run this script on the current system.", entonces debe ejecutar 

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.venv\Scripts\activate 
```

![python-16](images/python-16.png)


Si esta trabajando en MacOs o Linux, ejecute los siguientes comandos

```bash
source .venv/bin/activate
```

Luego, en la misma terminal ejecutamos el siguiente comando:

En Windows:

```bash
pip install -r requirements.txt
```

En MacOS/Linux:

```bash
pip3 install -r requirements.txt
```


Incluimos el siguiente código para conectarnos con Cloud FireStore y generar referencias a las Colecciones Estudiantes y Peticiones
```python
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app


app = Flask(__name__)

# Inicializar Firestore DB
cred = credentials.Certificate('key/key.json')
default_app = initialize_app(cred)
db = firestore.client()
estudiantes_ref = db.collection('Estudiantes')
peticiones_ref = db.collection('Peticiones')

if __name__ == '__main__':
    app.run(debug=True)
```

## Creación de Clases con Modelo de Datos

Vamos a generar dos Clases para nuestro modelo de datos (Estudiante y Petición), creamos una carpeta models y los archivos estudiante.py y peticion.py

> ¿Por qué usamos clases?

Para la instancia de Peticiones debemos incluir la fecha en la zona horaria correcta, importamos pytz, datetime y asignamos la zona horaria
```python
import pytz
from datetime import datetime

timezone = pytz.timezone("America/Bogota")
```

La clase de petición sería la siguiente:
```python
import pytz
from datetime import datetime

timezone = pytz.timezone("America/Bogota")

class Peticion:
    def __init__(self, cedula, peticion, fecha_atencion,estado = "Creada"):
        self.cedula = cedula
        self.peticion = peticion
        self.fecha_atencion = timezone.localize(datetime.strptime(fecha_atencion, '%d/%m/%y %H:%M:%S'))
        self.fecha_creacion = timezone.localize(datetime.now())
        self.estado = estado


    def to_dict(self):
        return dict((key, value) for (key, value) in self.__dict__.items())
```



> **Ejercicio**: Cree el modelo de Estudiante en el archivo estudiante.py dentro de la carpeta models, debe tener los siguiente campos: cedula, nombre, apellido, correo, carrera


Ahora vamos a crear un archivo __init__.py en la carpeta models para importar los dos modelos

```python
from .estudiante import Estudiante
from .peticion import Peticion
```

Importamos los modelos en el app.py

```python
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

from models import Estudiante,Peticion
```

Probemos crear una instancia de cada modelo para verificar que quedo bien
```python
nuevo_estudiante=Estudiante(122345, "Jaime", "Garcia", "jaime.garcia", "Electronica")
print(nuevo_estudiante.to_dict())
```


Ahora creamos una peticion de prueba
```python
nueva_peticion=Peticion(122345, "Asesoria",'25/09/20 7:00:00')
print(nueva_peticion.to_dict(),nueva_peticion.fecha_creacion,nueva_peticion.fecha_atencion)
```

El código completo que llevamos hasta el momento es el siguiente:


**models**

__init__.py
```python
from .estudiante import Estudiante
from .peticion import Peticion
```

estudiante.py
```python
class Estudiante:
    def __init__(self, cedula, nombre, apellido, correo, carrera):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.carrera = carrera

    def to_dict(self):
        return dict((key, value) for (key, value) in self.__dict__.items())
```

peticion.py
```python
import pytz
from datetime import datetime

timezone = pytz.timezone("America/Bogota")

class Peticion:
    def __init__(self, cedula, peticion, fecha_atencion,estado = "Creada"):
        self.cedula = cedula
        self.peticion = peticion
        self.fecha_atencion = timezone.localize(datetime.strptime(fecha_atencion, '%d/%m/%y %H:%M:%S'))
        self.fecha_creacion = timezone.localize(datetime.now())
        self.estado = estado


    def to_dict(self):
        return dict((key, value) for (key, value) in self.__dict__.items())
```

**root**

app.py
```python

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

if __name__ == '__main__':
    app.run(debug=True)
```


## Creación de Rutas para Estudiantes

### Agregar Estudiantes

Vamos a agregar la primera ruta: POST para Agregar nuevos estudiantes

```python
@app.route("/api/estudiantes",methods=['POST'])
def agregar_estudiante():

    data=request.json
    estudiante_id=str(request.json["cedula"])
    try:  
        nuevo_estudiante=Estudiante(data["cedula"], data["nombre"], data["apellido"],data["correo"], data["carrera"]).to_dict()
        estudiantes_ref.document(estudiante_id).set(nuevo_estudiante)
        return jsonify(nuevo_estudiante),201
    except:
        error_message={"error":"Los datos del estudiante no están completos o son incorrectos"}
        return jsonify(error_message),400
```

> ¿Qué pasa si volvemos a crear un estudiante con la misma cédula?

Nos falta validar si ya existe un documento con el mismo ID, en cuyo caso retornamos error
```python
@app.route("/api/estudiantes",methods=['POST'])
def agregar_estudiante():

    data=request.json
    estudiante_id=str(request.json["cedula"])
    estudiantes_doc=estudiantes_ref.document(estudiante_id)
    if(estudiantes_doc.get().exists):
        error_message={"error":f"Ya existe un estudiante registrando con el ID {estudiante_id}"}
        return jsonify(error_message),400
    try:  
        nuevo_estudiante=Estudiante(data["cedula"], data["nombre"], data["apellido"],data["correo"], data["carrera"]).to_dict()
        estudiantes_doc.set(nuevo_estudiante)
        return jsonify(nuevo_estudiante),201
    except:
        error_message={"error":"Los datos del estudiante no están completos o son incorrectos"}
        return jsonify(error_message),400
```

Si hacemos una consulta como la siguiente, se agregará un estudiante en la base de datos

```python
### Agregar nuevo estudiante
POST http://localhost:5000/api/estudiantes
Content-Type: application/json

{
  "cedula":2354659,
  "nombre":"Julian",
  "apellido":"Parras",
  "correo":"julian.parra@misena.edu.co",
  "carrera":"Industrial"
}
```

### Obtener Estudiantes

Ahora vamos a crear una ruta para obtener todos los estudiantes agregados

```python
@app.route("/api/estudiantes",methods=['GET'])
def obtener_lista_estudiantes():

    results=estudiantes_ref.stream()
    lista_estudiantes=[item.to_dict() for item in results]

    return jsonify({"data":lista_estudiantes}),200
```

Probamos con la siguiente petición en Rest Client

```python
### Listar todos los estudiantes
GET http://localhost:5000/api/estudiantes
```

Generemos una ruta para obtener un estudiante específico a partir de su cédula

```python
@app.route("/api/estudiantes/<int:id>",methods=['GET'])
def obtener_estudiante(id):

    estudiante_doc=estudiantes_ref.document(str(id)).get()
    if(estudiante_doc.exists):
      return jsonify(estudiante_doc.to_dict()),200
    else:
      error_message={"error":f"No se encontró ningún estudiante con el ID {id}"}
      return jsonify(error_message),400
```

Probamos con la siguiente petición en Rest Client

```python
### Obtener información de estudiante
GET http://localhost:5000/api/estudiantes/{{cedula}}
```


### Actualizar y Borrar Estudiantes

> Ejercicio: Crear las Rutas para Actualizar y Borrar Estudiantes con conexión a la base de datos y validación de errores

```python
@cedula2=2354659
Pruebe su código con las siguientes peticiones en REST Client o Postman

### Actualizar estudiante
PUT http://localhost:5000/api/estudiantes/{{cedula2}}
Content-Type: application/json

{
    "cedula":2354656,
    "nombre":"Julian",
    "apellido":"Parras",
    "correo":"julian.parras@misena.edu.co",
    "carrera":"Electrónica"
}


### Eliminar Estudiante
DELETE http://localhost:5000/api/estudiantes/{{cedula2}}
```
