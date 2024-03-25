# import logging
# import os
# from functools import wraps
# import firebase_admin
# from firebase_admin import credentials, auth
# from flask import Flask, request, jsonify, render_template, make_response, send_file
# from flask_talisman import Talisman
# from flask_cors import CORS
# from flask_restful import Api, Resource
# from pymongo import MongoClient
# from config import firebase_config
# from auth import authenticate

# app = Flask(__name__)  # Create Flask app
# api = Api(app)  # Create API
# CORS(app)  # Enable CORS
# Talisman(app)  # Enable HTTPS


# class Status(Resource):
#     def get(self):
#         try:
#             return {'data': 'Api is Running'}
#         except:
#             return {'data': 'An Error Occurred during fetching Api'}


# class MongoDBResource(Resource):
#     def __init__(self):
#         self.db = MongoClient(os.environ.get(
#             "MONGO_URI")).claspMobileDB
#         super().__init__()

#     @authenticate
#     def get(self, collection_name):
#         args = request.args.to_dict()
#         collection = self.db[collection_name]
#         documents = list(collection.find(args, {'_id': 0}))
#         return jsonify(documents)

#     @authenticate
#     def post(self, collection_name):
#         data = request.json
#         collection = self.db[collection_name]
#         result = collection.insert_one(data)
#         return {'id': str(result.inserted_id)}


# class ApiDocs(Resource):
#     def get(self):
#         html_content = render_template('docs.html')
#         response = make_response(html_content)
#         response.headers['Content-Type'] = 'text/html'
#         return response


# # Assuming your Flask app is launched from the 'service1' directory
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MEDIA_FOLDER = os.path.join(BASE_DIR, 'media-data')


# class MediaResource(Resource):
#     def get(self, task_dir, filename):
#         # Construct the full file path
#         file_path = os.path.join(MEDIA_FOLDER, task_dir, filename)

#         # Check if the file exists and is a file
#         if os.path.isfile(file_path):
#             return send_file(file_path)
#         else:
#             # Return a 404 not found response if the file doesn't exist
#             return "File not found", 404


# Setup the route
# api.add_resource(MediaResource, '/media-data/<path:task_dir>/<filename>')

# api.add_resource(Status, '/status')
# api.add_resource(MongoDBResource, '/api/<collection_name>/')
# api.add_resource(ApiDocs, '/docs')

# if __name__ == '__main__':
#     # port = int(os.environ.get("PORT", 5000))
#     # app.run(host='0.0.0.0', port=port)
#     app.run(debug=True)  # Run app

from app import create_app

app = create_app()
