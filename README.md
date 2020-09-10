# flask-rest-api



pip freeze > requirements.txt

git config user.name "Nombre de Usuario"


python3 -m venv env

Flask==1.1.2


pip3 install -r requirements.txt


from flask import Flask
app = Flask(__name__)


@app.route("/")
def hola_mundo():
  return "Hola, Mundo!"


# flask depends on this env variable to find the main file
export FLASK_APP=app.py

# now we just need to ask flask to run
flask run

# * Serving Flask app "hello"
# * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)