# from api import mongo
import os
from pymongo import MongoClient

db = MongoClient(os.environ.get('MONGO_URI')).adaptiveTextDB


def save_rephrased_text(original_text_id, current_text, rephrased_text, similarity_score, emotion_distance, rephrase_no):
    text_collection = db['logs']
    text_document = {
        'original_text_id': original_text_id,
        'current_text': current_text,
        'rephrased_text': rephrased_text,
        'similarity_score': similarity_score,
        'emotion_distance': emotion_distance,
        'rephrase_no': rephrase_no
    }
    text_collection.insert_one(text_document)
