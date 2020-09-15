


Vamos a incluir dos librerías en nuestro requirements.txt: firebase-admin para la conexión con bases de datos y pytz para el manejo de zonas horarias

```python
Flask==1.1.2
firebase-admin==4.3.0
pytz==2020.1
```
Debemos tener activo el entorno virtual, si no lo tenemos- Hacemos click en Terminal y ejecutamos los siguientes comandos:

```bash
.\venv\Scripts\activate
```

![python-15](images/python-15.png)

Si se genera el mensaje "Activate.ps1 is not digitally signed. You cannot run this script on the current system.", entonces debe ejecutar 

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
source .venv/bin/activate
```

![python-16](images/python-16.png)


Si esta trabajando en MacOs o Linux, ejecute los siguientes comandos

```bash
python3 -m venv .venv
source .venv/bin/activate

Luego, en la misma terminal ejecutamos el siguiente comando:

En Windows:

```bash
pip install -r requirements.txt
```

En MacOS/Linux:

```bash
pip3 install -r requirements.txt
```




Inclumos el siguiente código para conectarnos con Cloud FireStore y generar referencias a las Colecciones Estudiantes y Peticiones
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

Vamos a generar dos Clases para nuestro modelo de datos (Estudiante y Petición), creamos una carpeta models y los archivos estudiante.py y peticion.py


Para la instancia de Peticiones debemos incluir la fecha en la zona horaria correcta, importamos pytz, datetime y asignamos la zona horaria
```python
import pytz
from datetime import datetime

timezone = pytz.timezone("America/Bogota")
```

La clase de petición sería la siguiente:
```python
class Peticion:
    def __init__(self, cedula, peticion, fecha_atencion):
        self.cedula = cedula
        self.peticion = peticion
        self.fecha_atencion = timezone.localize(datetime.strptime(fecha_atencion, '%d/%m/%y %H:%M:%S'))
        self.fecha_creacion = timezone.localize(datetime.now())


    def to_dict(self):
        return dict((key, value) for (key, value) in self.__dict__.items())
```



Ejercicio: Cree el modelo de Estudiante en el archivo estudiante.py dentro de la carpeta models, debe tener los siguiente campos: cedula, nombre, apellido, correo, carrera


Ahora vamos a crear un archivo __init__.py para importar los dos modelos

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


Vamos a agregar la primera ruta: POST para Agregar nuevos estudiantes

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


Request

Metadata about the request
• Content Type: The format of Content
• Content Length: Size of Content
• Authorization: Who’s making the call
• Accept: What type(s) can accept
• Cookies: Passenger data in the request
• More headers…


Content Concerning Request
• HTML, CSS, JavaScript, XML, JSON
• Content is not valid with some verbs
• Information to help fulfill request
• Binary and blobs common (e.g. .jpg)


Response


Operation Status
• 100-199: Informational
• 200-299: Success
• 300-399: Redirection
• 400-499: Client Errors
• 500-599: Server Errors


Metadata about the response
• Content Type: The format of Content
• Content Length: Size of Content
• Expires: When to consider stale
• Cookies: Passenger data in the request
• More headers…

Content
• HTML, CSS, JavaScript, XML, JSON
• Binary and blobs common (e.g. .jpg)
• APIs often have their own types


Versionado

Should You Version Your API?
- Once you publish, it’s set in stone
- Users rely on the API not changing
- But requirements will change


/v1/estudiantes/1324345/tareas


Ejercicio: Crear las Rutas para Put and Delete con Conexión a la base de datos y validación



