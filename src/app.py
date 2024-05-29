from flask import Flask, request, jsonify, render_template, send_file
from deep_translator import GoogleTranslator
from gtts import gTTS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app) 

# Retrieve MongoDB connection details from environment variables
mongodb_uri = os.getenv('MONGODB_URI')

# Initialize MongoDB client
client = MongoClient(mongodb_uri)
db = client.get_database()

# Initialize the counter collection if it doesn't exist
if db.counters.count_documents({'_id': 'translator_history_id'}, limit=1) == 0:
    db.counters.insert_one({'_id': 'translator_history_id', 'sequence_value': 0})

def get_next_sequence_value(sequence_name):
    counter = db.counters.find_one_and_update(
        {'_id': sequence_name},
        {'$inc': {'sequence_value': 1}},
        return_document=True
    )
    return counter['sequence_value']

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    input_text = data.get('text')
    input_lang = data.get('inputLang')
    output_lang = data.get('outputLang')
    
    translator = GoogleTranslator(source=input_lang, target=output_lang)
    translated_text = translator.translate(input_text)
    
    return jsonify({'translated_text': translated_text})

@app.route('/saveword', methods=['POST'])
def saveword():
    data = request.get_json()
    input_text = data.get('input_text')
    output_text = data.get('output_text')
    input_lang = data.get('input_lang')
    output_lang = data.get('output_lang')

    
    # Get the next sequence value for _id
    next_id = get_next_sequence_value('translator_history_id')
    db.TranslatorHistory.insert_one({'_id': next_id, 'input_text': input_text, 'output_text': output_text, 'input_lang': input_lang, 'output_lang': output_lang })
    
    # Ensure only the last 10 entries are kept
    if db.TranslatorHistory.count_documents({}) > 10:
        oldest_entry = db.TranslatorHistory.find().sort('_id', 1).limit(1)
        db.TranslatorHistory.delete_one({'_id': oldest_entry[0]['_id']})
    
    return jsonify({'success': True})

@app.route('/last_words', methods=['GET'])
def last_words():
    words = list(db.TranslatorHistory.find().sort('_id', -1).limit(10))
    return jsonify(words)


@app.route('/tts', methods=['POST'])
def tts():
    data = request.get_json()
    translated_text = data.get('text')
    output_lang = data.get('outputLang')
    if not translated_text:
        return jsonify({'error': 'Translated text is missing.'}), 400

    # Generate TTS for translated text
    tts = gTTS(text=translated_text, lang=output_lang)
    tts_file = 'translated_text.mp3'

    if os.path.exists(tts_file):
        os.remove(tts_file)
    tts.save(tts_file)

    # Serve TTS audio file
    response = send_file(tts_file, mimetype='audio/mpeg')

    return jsonify({'tts_filename': f'{tts_file}'})

@app.route('/get_tts', methods=['GET'])
def get_tts():
    tts_filename = request.args.get('filename')
    if not tts_filename:
        return jsonify({'error': 'Filename is missing.'}), 400

    tts_file_path = os.path.join('.', tts_filename)
    if not os.path.exists(tts_file_path):
        return jsonify({'error': 'File not found.'}), 404
    print(tts_filename)
    return send_file(tts_filename, mimetype='audio/mpeg')


if __name__ == '__main__':
    app.run(debug=True)
