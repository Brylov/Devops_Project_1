import ast
import codecs
from flask import json
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"English to Japanese Translator" in response.data

def test_translation(client):
    response = client.post('/translate', json={'text': 'hello'})
    assert response.status_code == 200
    parsed_data = json.loads(response.data)
    translated_text_unicode = parsed_data['translated_text']
    # Decode the Unicode escape sequence to obtain the Japanese characters
    japanese_string = ast.literal_eval('"' + translated_text_unicode + '"')
    # Print response data to console
    assert japanese_string == "こんにちは"

#page not exist check
