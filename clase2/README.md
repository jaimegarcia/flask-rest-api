# Módulo 3 Introducción a las arquitecturas y desarrollo con API Rest 
# Clase 2 

# Tabla de Contenido

<!-- toc -->

- [Hola Mundo en Flask](#hola-mundo-en-flask)
- [Instalación de Rest Client o Postman](#instalación-de-rest-client-o-postman)


<!-- tocstop -->

## Hola Mundo en Flask

Partiendo, del proyecto generado en la Clase 1. Adicione en el archivo app.py, una función que retorne algun contenido, en este caso, un string; use, además, el decorador app.route para mapear la ruta del URL / a esa función:

```python
@app.route("/")
def hola_mundo():
  return "Hola, Mundo!"
```
Guarde la aplicación app.py (cmd/ctrl S).

En la terminal, ejecute la aplicación mediante el comando:

En Windows:
```bash
python -m flask run --reload
```

En MacOS/Linux
```bash
python3 -m flask run --reload
```

O también puede ejecutar
```bash
python app.py
```

El servidor busca la aplicacción app.py por defecto. Al correr Flask, verá una salida similar a la siguiente:
```bash
(env) python -m flask run --reload
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Abrimos en un navegador la ruta localhost:5000, y debemos ver el mensaje Hola, Mundo!

Cambiemos algo del código

```python
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hola_mundo():
  return "Adios, Mundo!"
```

Se actualizará automáticamente, y si ingresamos de nuevo a la ruta en el navegador, veremos el nuevo mensaje.

Agreguemos una nueva ruta pero con un parámetro. La f indica un string con formato, el nombre es reemplazado por el parámetro que recibe la función

```python
@app.route("/saludo/<nombre>")
def saludo(nombre):
  return f"Hola {nombre}"
```

Podemos indicar el tipo de dato que va a recibir la ruta de la siguiente forma:

```python
@app.route("/saludo/<string:nombre>")
def saludo(nombre):
  return f"Hola {nombre}"
```

Agregemos un parámetro dentro de la query de la ruta: titulo.

Primero debemos importar request de Flask
```python
from flask import Flask,request
```

```python
@app.route("/saludo/<string:nombre>")
def saludo(nombre):
  titulo = request.args.get('titulo', '')
  return f"Hola {titulo} {nombre}"
```

En un navegador ingresamos la ruta incluyendo el parámetro, la respuesta que obtenemos 

```
http://localhost:5000/saludo/jaime?titulo=Sr
```


Así queda el código con estas dos rutas:

```python
from flask import Flask,request
import sys

app = Flask(__name__)

@app.route("/")
def hola_mundo():
  print("holas")
  return "Adiós, Mundo!"


@app.route("/saludo/<string:nombre>")
def saludo(nombre):
  titulo = request.args.get('titulo', '')
  return f"Hola {titulo} {nombre}"

if __name__ == '__main__':
    app.run(debug=True)
```

> **Ejercicio**: Agregue una nueva ruta que se llame despedida, deb recibir como dentro de la ruta un string el nombre de la persona y un parámetro con el tipo de frase de despedida (Chao, Adiós, Sayonara). Es decir que si se ingresa a la ruta /despedida/jaime?tipo=Sayonara la respuesta que debemos obtener es Sayonara jaime


### Instalación de Rest Client o Postman

Vamos a utilizar un Cliente para conectarnos con las APIs que se van a crear. Se recomienda la extensión Rest Client de VSCode. 

Para instalar Rest Client, vaya a extensiones en VSCode busque Rest Client, haga click en Instalar y Recargue VSCode

![rest-client](images/rest-client.png)


También puede utilizar Postman. Para instalar Postman, ingrese a https://www.postman.com/, registrese y descargué el producto

Incluyamos las rutas que usamos antes

```python
### Hola Mundo
GET http://localhost:5000/

### Saludo
GET http://localhost:5000/saludo/jaime?titulo=Sr
```
