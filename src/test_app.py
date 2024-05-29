import os
import pytest
import json
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_translate_endpoint(client):
    response = client.post('/translate', json={'text': 'hello', 'inputLang': 'en', 'outputLang': 'ja'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'translated_text' in data


def test_last_words_endpoint(client):
    response = client.get('/last_words')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_tts_endpoint(client):
    response = client.post('/tts', json={'text': 'こんにちは', 'outputLang': 'ja'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'tts_filename' in data

def test_get_tts_endpoint(client):
    response = client.get('/get_tts?filename=translated_text.mp3')
    assert response.status_code == 200

def test_saveword_and_deleteword_endpoint(client):
    # First, let's add a word to the database for testing
    response = client.post('/saveword', json={'input_text': 'hello', 'output_text': 'こんにちは', 'input_lang': 'English', 'output_lang': 'Japanese'})
    assert response.status_code == 200
    # Decode the byte object into a string and parse as JSON
    data = json.loads(response.data.decode('utf-8'))

    # Access the word data from the response
    saved_word_data = data.get('word')

    assert data['success'] == True
    assert 'id' in saved_word_data
    
    word_id = saved_word_data['id']  # Get the ID of the newly added word
    
    # Now, let's try to delete the word using the obtained ID
    response = client.delete(f'/deleteword/{word_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    
    # Check if the word was actually deleted by attempting to retrieve it
    response = client.get(f'/getword/{word_id}')
    assert response.status_code == 404  # Expecting a 404 since the word should no longer exist

    # Test deleting a non-existent word
    response = client.delete('/deleteword/1000')
    assert response.status_code == 404
