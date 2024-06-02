from flask import Flask, request, jsonify, render_template, send_file
from deep_translator import GoogleTranslator
from gtts import gTTS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)
# Check if running in a test environment (e.g., Jenkins)
is_test_environment = os.environ.get('JENKINS_TEST')


if not is_test_environment:
    # Get MongoDB service DNS name from environment variable
    mongo_service_dns = os.environ.get('MONGO_SERVICE_DNS')
    
else:
    # If running in a test environment, set a default value for MongoDB service DNS
    mongo_service_dns = 'mongodb'
    

username = os.environ.get('MONGO_USERNAME')  # Replace 'your_username' with your MongoDB username
password = os.environ.get('MONGO_PASSWORD')
database = os.environ.get('MONGO_DB') # Replace 'your_password' with your MongoDB password
mongodb_uri = f'mongodb://{username}:{password}@{mongo_service_dns}:27017/{database}'
print(f'Establish connection to {mongodb_uri}')

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
    
    # Insert the word into the database
    db.TranslatorHistory.insert_one({'_id': next_id, 'input_text': input_text, 'output_text': output_text, 'input_lang': input_lang, 'output_lang': output_lang })
    
    # Ensure only the last 10 entries are kept
    if db.TranslatorHistory.count_documents({}) > 10:
        oldest_entry = db.TranslatorHistory.find().sort('_id', 1).limit(1)
        db.TranslatorHistory.delete_one({'_id': oldest_entry[0]['_id']})
    
    # Return the saved word data in the response
    saved_word = {
        'id': next_id,
        'input_text': input_text,
        'output_text': output_text,
        'input_lang': input_lang,
        'output_lang': output_lang
    }
    
    return jsonify({'success': True, 'word': saved_word})

@app.route('/last_words', methods=['GET'])
def last_words():
    words = list(db.TranslatorHistory.find().sort('_id', -1).limit(10))
    return jsonify(words)

app.route('/getword/<word_id>', methods=['GET'])
def get_word(word_id):
    try:
        # Convert word_id to integer
        word_id = int(word_id)
        
        # Query the database for the word with the given ID
        word = db.TranslatorHistory.find_one({'_id': word_id})
        
        if word:
            # If the word exists, return it as JSON response
            return jsonify({'success': True, 'word': word}), 200
        else:
            # If word not found, return error response
            return jsonify({'success': False, 'error': 'Word not found.'}), 404
    except ValueError:
        # If word ID format is invalid, return error response
        return jsonify({'success': False, 'error': 'Invalid word ID format.'}), 400
    except Exception as e:
        # If any other error occurs, return error response
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/tts', methods=['POST'])
def tts():
    data = request.get_json()
    text = data.get('text')
    lang = data.get('lang')
    if not text:
        return jsonify({'error': 'Translated text is missing.'}), 400

    # Generate TTS for translated text
    tts = gTTS(text=text, lang=lang)
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

@app.route('/deleteword/<word_id>', methods=['DELETE'])
def deleteword(word_id):
    try:
        # Convert word_id to integer
        word_id = int(word_id)
        
        # Check if the word exists in the database
        word = db.TranslatorHistory.find_one({'_id': word_id})
        if word:
            # Delete the word from the database
            db.TranslatorHistory.delete_one({'_id': word_id})
            return jsonify({'success': True, 'message': 'Word deleted successfully.'}), 200
        else:
            return jsonify({'success': False, 'error': 'Word not found.'}), 404
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid word ID format.'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'success': True, 'message': 'Health Check Okay'}), 200

if __name__ == '__main__':
    app.run(debug=True)
