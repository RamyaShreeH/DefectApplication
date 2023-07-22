from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request

app = Flask(__name__)

app.secret_key = "secretkey"

app.config['MONGO_URI'] = "mongodb://localhost:27017/db1"

mongo = PyMongo(app)

@app.route('/application/add', methods = ['POST'])
def add():
    _json = request.json
    _name = _json['name']
    _email = _json['email']

    if _name and _email and request.method == 'POST':
        id = mongo.db.db1.insert_one({'name': _name, 'email': _email})
        response = jsonify("Added Successfully")
        response.status_code = 200
        return response
    
    else:
        return not_found()

@app.route('/application/getAll')
def get_all_data():
    applications = mongo.db.db1.find()
    response = dumps(applications)
    return response

@app.route('/application/getById/<id>')
def get_by_id(id):
    application = mongo.db.db1.find_one({'_id':ObjectId(id)})
    response = dumps(application)
    return response

@app.route('/application/delete/<id>')
def delete(id):
    mongo.db.db1.delete_one({'_id':ObjectId(id)})
    response = jsonify("Deleted Successfully")
    response.status_code = 200
    return response

@app.route('/application/update/<id>', methods = ['PUT'])
def update(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']

    if _name and _email and _id and request.method == 'PUT':
        mongo.db.db1.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
        {'$set':{'name': _name, 'email': _email}})
        response = jsonify("Updated Successfully")
        response.status_code = 200
        return response
    
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error = None):
    message = {
        'status':404,
        'message':'Not Found' + request.url
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ =='__main__': 
    app.run(debug = True)