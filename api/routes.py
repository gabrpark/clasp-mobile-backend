import os
from flask import Blueprint, Flask, request, jsonify
# from flask_restful import Resource # Use this to create a RESTful API
from pymongo import MongoClient
from api.utils.auth import authenticate
# from bson.objectid import ObjectId

db = MongoClient(os.environ.get("NGROK_MONGO_URL"))

api_bp = Blueprint('api', __name__)


@api_bp.route('/')
def status():
    try:
        return {'data': 'Api is Running'}
    except:
        return {'data': 'An Error Occurred during fetching Api'}


@api_bp.route('/tasks', methods=['GET'])
@authenticate
def get_all_tasks():
    args = request.args.to_dict()
    collection = db['tasks']
    documents = list(collection.find(args, {'_id': 0}))
    return jsonify(documents)

# TODO: This is a sample code, the front end need to be updated to use this.
# @api_bp.route('/tasks/<task_id>', methods=['GET'])
# @authenticate
# def get_task(task_id):
#     task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
#     if task:
#         task['_id'] = str(task['_id'])
#         return jsonify(task)
#     else:
#         return jsonify({'message': 'Task not found'}), 404


@api_bp.route('/responses', methods=['POST'])
@authenticate
def post_response():
    data = request.json
    collection = db['responses']
    result = collection.insert_one(data)
    # TODO: ML can be called here to process the data if real time prediction is desired.
    return {'id': str(result.inserted_id)}
