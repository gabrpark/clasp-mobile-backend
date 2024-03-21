import logging
import os
from functools import wraps
import firebase_admin
from firebase_admin import credentials, auth
from flask import Flask, request, jsonify, render_template
# from flask_talisman import Talisman
from flask_cors import CORS
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__, template_folder='./static')  # Create Flask app
api = Api(app)  # Create API
CORS(app)  # Enable CORS
# Talisman(app)  # Enable HTTPS

firebase_config = {
    "type": os.environ.get("FIREBASE_TYPE"),
    "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
    "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace(r'\n', '\n'),
    "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
    "auth_uri": os.environ.get("FIREBASE_AUTH_URI"),
    "token_uri": os.environ.get("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.environ.get("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_X509_CERT_URL"),
    "universe_domain": os.environ.get("FIREBASE_UNIVERSE_DOMAIN")
}

# Initialize Firebase Admin
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        id_jwt_token = request.headers.get('Authorization')
        if not id_jwt_token:
            return {'status': 'error', 'message': 'Authorization token missing'}, 401

        try:
            decoded_token = auth.verify_id_token(id_jwt_token, check_revoked=True)
            request.user = decoded_token
            return f(*args, **kwargs)
        except auth.RevokedIdTokenError:
            logging.error('Token revoked')
            return {'status': 'error', 'message': 'Token has been revoked'}, 401
        except auth.InvalidIdTokenError:
            logging.error('Invalid token')
            return {'status': 'error', 'message': 'Invalid token'}, 401
        except Exception as e:
            logging.error('Authentication error: %s', str(e))
            return {'status': 'error', 'message': 'Authentication error'}, 500

    #return decorated_function
    return decorated_function 


class Status(Resource):
    def get(self):
        try:
            return {'data': 'Api is Running'}
        except:
            return {'data': 'An Error Occurred during fetching Api'}


class MongoDBResource(Resource):
    def __init__(self):
        self.db = MongoClient(os.environ.get(
            "MONGO_URI")).claspMobileDB
        super().__init__()

    #@authenticate
    def get(self, collection_name):
        args = request.args.to_dict()
        collection = self.db[collection_name]
        documents = list(collection.find(args, {'_id': 0}))
        return jsonify(documents)

    #@authenticate
    def post(self, collection_name):
        data = request.json
        collection = self.db[collection_name]
        result = collection.insert_one(data)
        return {'id': str(result.inserted_id)}

class ApiDocs(Resource):
    def get(self):
        return render_template('index.html')

api.add_resource(Status, '/status')
api.add_resource(MongoDBResource, '/api/<collection_name>/')
api.add_resource(ApiDocs, '/doc')

if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(debug=True)  # Run app
