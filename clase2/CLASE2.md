


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
import os
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

Vamos a generar dos Clases para nuestro modelo de datos (Estudiantes y Peticiones), creamos una carpeta models y un archivo estudiantes.py

La clase de estudiantes sería la siguiente:
```python
class Estudiante:
    def __init__(self, cedula, nombre, apellido, correo, carrera):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.carrera = carrera
```

Ejercicio: Cree el modelo de Peticion en el archivo peticion.py dentro de la carpeta models, debe tener los siguiente campos: cedula, peticion, fecha_creacion, fecha_atencion


Ahora vamos a crear un archivo __init__.py para importar los dos modelos

```python
from .estudiante import Estudiante
from .peticion import Peticion
```

Importamos los modelos en el app.py

```python
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

from models import Estudiante,Peticion
```

Probemos crear una instancia de cada modelo para verificar que quedo bien
```python
nuevo_estudiante=Estudiante(122345, "Jaime", "Garcia", "jaime.garcia", "Electronica")
print(nuevo_estudiante)
```


Para la instancia de Peticiones debemos incluir la fecha en la zona horaria correcta, importamos pytz, datetime y asignamos la zona horaria
```python
import pytz
from datetime import datetime

timezone = pytz.timezone("America/Bogota")
```

Ahora creamos una peticion de prueba
```python
nueva_fecha_creacion=timezone.localize(datetime.now())
nueva_fecha_atencion=timezone.localize(datetime.strptime('25/09/20 7:00:00', '%d/%m/%y %H:%M:%S'))

nueva_peticion=Peticion(122345, "Asesoria",nueva_fecha_creacion,nueva_fecha_atencion)
print(nueva_peticion,nueva_peticion.fecha_creacion,nueva_peticion.fecha_atencion)
```

El código completo que llevamos hasta el momento es el siguiente:
```python

import os
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
print(nuevo_estudiante)

nueva_fecha_creacion=timezone.localize(datetime.now())
nueva_fecha_atencion=timezone.localize(datetime.strptime('25/09/20 7:00:00', '%d/%m/%y %H:%M:%S'))

nueva_peticion=Peticion(122345, "Asesoria",nueva_fecha_creacion,nueva_fecha_atencion)
print(nueva_peticion,nueva_peticion.fecha_creacion,nueva_peticion.fecha_atencion)

if __name__ == '__main__':
    app.run(debug=True)
```

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