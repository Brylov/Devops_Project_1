import ast
import os
from flask import json
import pytest
from app import app
from pymongo import MongoClient, errors
from dotenv import load_dotenv


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

def test_page_not_exist(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404

def test_mongo_connectivity():
    load_dotenv()
    mongodb_uri = os.getenv('MONGODB_URI')
    
    if not mongodb_uri:
        pytest.fail("MONGODB_URI environment variable not set")
    
    try:
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        client.server_info()  # Forces a call to the server to check connection
        assert True
    except errors.ServerSelectionTimeoutError:
        pytest.fail("Could not connect to MongoDB")

