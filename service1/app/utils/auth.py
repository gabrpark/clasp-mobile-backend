import logging
from functools import wraps
import firebase_admin
from firebase_admin import credentials, auth
from flask import request
from app.config import firebase_config

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
            decoded_token = auth.verify_id_token(
                id_jwt_token, check_revoked=True)
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

    return decorated_function
