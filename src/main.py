"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Todos
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/maintodos', methods=['GET'])
def main_todos():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

#Get all todos#

@app.route('/mytodos', methods=['GET'])
def get_todos():
    mis_todos = Todos.query.all()
    all_todos = list(map(lambda x: x.serialize(), mis_todos))
    return jsonify(all_todos), 200

#Get todo by id#
@app.route('/mytodos/<id>', methods=['GET'])
def one_todo(id):
    one_todo = Todos.query.filter_by(id=id).first()
    if not one_todo:
        return APIException("No se encontró la tarea",status_code=404)
    request_body = one_todo.serialize()
    return jsonify(request_body),200


#Post todo

@app.route('/mytodos', methods=['POST'])
def create_todo():
    data = request.get_json()
    mytodo = Todos(label=data["label"],done=data["done"]) #is_active=data["is_active"]
    db.session.add(mytodo)
    db.session.commit()
    return jsonify ("Message : Se adiciono una nueva tarea!"), 200


#Eliminar todo

@app.route('/mytodos/<id>', methods=['DELETE'])
def delete_mytodo(id):
    my_todo =  Todos.query.get(id)
    if not one_todo:
        return APIException("No se encontró la tarea",status_code=404)
    db.session.delete(my_todo)
    db.session.commit() 
    return jsonify("Succesfully eliminated!"), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
