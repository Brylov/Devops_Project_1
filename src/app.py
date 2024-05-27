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
        return jsonify({'error': 'Both English and translated text are required.'}), 400
    
    db.TranslatorHistory.insert_one({'english_text': english_text, 'translated_text': translated_text})
    return jsonify({'success': True})

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
