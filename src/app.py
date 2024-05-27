from flask import Flask, request, jsonify, render_template, send_file
from deep_translator import GoogleTranslator
from gtts import gTTS
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    english_text = data.get('text')
    if not english_text:
        return jsonify({'error': 'Text to translate is missing.'}), 400
    
    translator = GoogleTranslator(source='en', target='ja')
    translated_text = translator.translate(english_text)
    
    return jsonify({'translated_text': translated_text})

@app.route('/saveword', methods=['POST'])
def saveword():
    data = request.get_json()
    english_text = data.get('english_text')
    translated_text = data.get('translated_text')
    if not english_text or not translated_text:
        return jsonify({'error': 'Text to save is missing.'}), 400
    
    # Get the next sequence value for _id
    next_id = get_next_sequence_value('translator_history_id')
    db.TranslatorHistory.insert_one({'_id': next_id, 'english_text': english_text, 'translated_text': translated_text})
    
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
    if not translated_text:
        return jsonify({'error': 'Translated text is missing.'}), 400

    # Generate TTS for translated text
    tts = gTTS(text=translated_text, lang='ja')
    tts_file = 'translated_text.mp3'

    if os.path.exists(tts_file):
        os.remove(tts_file)
    tts.save(tts_file)

    # Serve TTS audio file
    response = send_file(tts_file, mimetype='audio/mpeg')

    # return jsonify({'tts_url': response})

    return jsonify({'tts_url': '/get_tts'})

@app.route('/get_tts')
def get_tts():
    return send_file('translated_text.mp3', mimetype='audio/mpeg')



if __name__ == '__main__':
    app.run(debug=True)
