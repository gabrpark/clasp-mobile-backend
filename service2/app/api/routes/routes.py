import os
from flask import Blueprint, jsonify, request
from pymongo import MongoClient
# from app.api.utils.auth import authenticate
from app.adaptator import Adaptator
from app.api.models.models import save_rephrased_text, db

api_bp = Blueprint('api', __name__)


@api_bp.route('/status', methods=['GET'])
def get_status():
    try:
        return jsonify({'data': 'API is Running'}), 200
    except Exception as e:
        # Logging the exception can be helpful for debugging
        print(f"Error occurred: {e}")
        return jsonify({'data': 'An Error Occurred during fetching API'}), 500


@api_bp.route('/texts', methods=['GET'])
# @authenticate
def get_tasks():
    args = request.args.to_dict()
    collection = db['sourceTexts']
    documents = list(collection.find(args, {'_id': 0}))
    return jsonify(documents)


@api_bp.route('/rephrase', methods=['GET'])
# @authenticate
def get_rephrase():
    data = request.get_json()

    original_text_id = data.get('original_text_id')

    current_text = data.get('current_text')
    selected_sentence_index = data.get('selected_sentence_index')
    current_emotion = data.get('current_emotion')
    target_emotion = data.get('target_emotion')

    rephrase_no = data.get('rephrase_no')

    # Testing data for the rephraser API without parameters.
    # original_text_id = 0
    # current_text = ("In mathematics, the Hodge conjecture is a major unsolved problem in algebraic geometry and complex geometry "
    #                 "that relates the algebraic topology of a non-singular complex algebraic variety to its subvarieties.")
    # selected_sentence_index = 0
    # current_emotion = 'neutral'
    # target_emotion = 'touched'
    # rephrase_no = 0

    # emotion_distance = embedder.calculate_distance(current_emotion, target_emotion)

    adpt = Adaptator(current_text, selected_sentence_index,
                     current_emotion, target_emotion)

    rephrased_text, similarity_score, emotion_distance = adpt.adapt()

    # Save the rephrased text to the database
    save_rephrased_text(original_text_id, current_text, rephrased_text,
                        similarity_score, emotion_distance, rephrase_no)

    # return jsonify({
    #     'original_text_id': original_text_id,
    #     'current_text': current_text,
    #     'rephrased_text': rephrased_text,
    #     'similarity_score': similarity_score,
    #     'emotion_distance': emotion_distance,
    #     'rephrase_no': rephrase_no
    # })

    return jsonify({
        'data': 'The rephrased text has been saved to the database.'
    })
