from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request

app = Flask(__name__)

app.secret_key = "secretkey"

app.config['MONGO_URI'] = "mongodb://localhost:27017/db1"

mongo = PyMongo(app)

# Add the application.
@app.route('/application', methods = ['POST'])
def add():
    json = request.json
    name = json['name']
    email = json['email']

    if name and email:
        id = mongo.db.db1.insert_one({'name': name, 'email': email, 'isDeleted': 'False'})
        response = jsonify("New application added successfully")
        response.status_code = 200
        # TODO: return ID of new application
        return response
    else:
        return not_found()

# Gets the list of application.
@app.route('/applications', methods = ['GET'])
def get_all_applicatios():
    applications = mongo.db.db1.find()
    response = dumps(applications)
    return response

# Get the application by id.
@app.route('/application/<id>', methods = ['GET'])
def get_by_id(id):
    application = mongo.db.db1.find_one({'_id':ObjectId(id)})
    response = dumps(application)
    return response

# Delete the application by id.
@app.route('/application/<id>', methods = ['DELETE'])
def delete(id):
    _id = id
    if _id:
        mongo.db.db1.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
        {'$set':{'isDeleted': 'True'}})
        response = jsonify("Deleted application successfully")
        response.status_code = 200
        return response

#Update the application by id.
@app.route('/application/<id>', methods = ['PUT'])
def update(id):
    _id = id
    json = request.json
    name = json['name']
    email = json['email']
    if name and email and _id:
        mongo.db.db1.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
        {'$set':{'name': name, 'email': email}})
        response = jsonify("Updated successfully")
        response.status_code = 200
        return response
    else:
        return not_found()


#separate comments table

# Adds comments.
@app.route('/comment', methods = ['POST'])
def addComment():
    json = request.json
    description = json['description']
    applicationId = json['applicationId']
    if description and applicationId:
        id = mongo.db.comment.insert_one({'description': description , 'applicationId': applicationId, 'isDeleted': 'False'})
        response = jsonify("New comment added successfully")
        response.status_code = 200
        # TODO: return ID of new application
        return response
    else:
        return not_found()

# Returns all comments.
@app.route('/comments', methods = ['GET'])
def get_all_comments():
    comments = mongo.db.comment.find()
    response = dumps(comments)
    return response

# Get by comment id.
@app.route('/comment/<id>', methods = ['GET'])
def get_by_componentid(id):
    comment = mongo.db.comment.find_one({'_id':ObjectId(id)})
    print("Comment:", comment)
    response = dumps(comment)
    return response

# Get by application id.
@app.route('/commentByApplicationId/<application_id>', methods = ['GET'])
def get_by_applicationid(application_id):
    comment = mongo.db.comment.find({'applicationId': application_id})
    print("Comment By appliaction Id:", comment)
    response = dumps(comment)
    return response


# Delete by comment id
@app.route('/comment/<id>', methods = ['DELETE'])
def deleteComment(id):
    _id = id
    if _id:
        mongo.db.comment.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
        {'$set':{'isDeleted': 'True'}})
        response = jsonify("Deleted application successfully")
        response.status_code = 200
        return response

# Update by comment id
@app.route('/comment/<id>', methods = ['PUT'])
def updateComment(id):
    _id = id
    json = request.json
    description = json['description']
    applicationId = json['applicationId']
    if description and applicationId and _id:
        mongo.db.comment.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
        {'$set':{'description': description, 'applicationId': applicationId}})
        response = jsonify("Comment updated successfully")
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