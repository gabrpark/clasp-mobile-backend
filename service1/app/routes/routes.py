import os
from flask import Blueprint, jsonify, request, send_file, abort
from pymongo import MongoClient
from app.utils.auth import authenticate
from werkzeug.utils import safe_join

db = MongoClient(os.environ.get('MONGO_URI')).claspMobileDB

api_bp = Blueprint('api', __name__)


@api_bp.route('/status', methods=['GET'])
def get_status():
    try:
        return jsonify({'data': 'API is Running'}), 200
    except Exception as e:
        # Logging the exception can be helpful for debugging
        print(f"Error occurred: {e}")
        return jsonify({'data': 'An Error Occurred during fetching API'}), 500


@api_bp.route('/tasks', methods=['GET'])
@authenticate
def get_tasks():
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
    return {'id': str(result.inserted_id)}


RELATIVE_PATH_FROM_CURRENT_FILE = '../../data/media'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_FOLDER = os.path.join(BASE_DIR, RELATIVE_PATH_FROM_CURRENT_FILE)


@api_bp.route('/data/media/<path:subpath>/<filename>', methods=['GET'])
# @authenticate
def serve_file(subpath, filename):
    # Prevent directory traversal & validate paths
    # Removes leading slashes to prevent absolute path
    secure_subpath = safe_join('', subpath)
    secure_filename = safe_join('', filename)  # Ensure filename is secure

    if secure_subpath is None or secure_filename is None:
        abort(400, "Invalid path or filename")

    # Construct the full file path
    file_path = os.path.join(MEDIA_FOLDER, subpath, filename)

    # Check if the file exists and is a file
    if os.path.isfile(file_path):
        return send_file(file_path)
    else:
        # Return a 404 not found response if the file doesn't exist
        return "File not found", 404

# TODO: This is a sample code for uploading facial video, the front end need to be updated to use this.
# UPLOAD_FOLDER = 'data/media/responses/videos'
# ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'flv', 'wmv'}


# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/upload/video', methods=['POST'])
# @authenticate
# def upload_video():
#     if 'video' not in request.files:
#         return abort(400, description="No video part in the request")

#     video = request.files['video']

#     if video.filename == '':
#         return abort(400, description="No video selected for upload")

#     if video and allowed_file(video.filename):
#         filename = secure_filename(video.filename)
#         save_path = os.path.join(UPLOAD_FOLDER)

#         os.makedirs(save_path, exist_ok=True)  # Ensure the directory exists

#         video_path = os.path.join(save_path, filename)
#         video.save(video_path)
#         return jsonify({"message": "Video uploaded successfully", "path": video_path})

#     return abort(400, description="Unsupported video format")
