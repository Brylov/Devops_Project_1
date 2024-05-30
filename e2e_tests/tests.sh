#!/bin/bash

set -e

# URL of your frontend and backend
FRONTEND_URL="http://localhost"
BACKEND_URL="http://localhost:5000/"

# Test 1: Check if the frontend is up
response=$(curl --write-out "%{http_code}\n" --silent --output /dev/null $FRONTEND_URL)
if [ "$response" -ne 200 ]; then
  echo "Frontend is not reachable. HTTP Status: $response"
  exit 1
fi
echo "Frontend is reachable."

# Test 2: Check if the backend is up
response=$(curl --write-out "%{http_code}\n" --silent --output /dev/null "$BACKEND_URL/healthcheck")
echo "$response"
if [ "$response" -ne 200 ]; then
  echo "Backend is not reachable. HTTP Status: $response"
  exit 1
fi
echo "Backend is reachable."


translation_response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"text": "hello", "inputLang": "en", "outputLang": "ja"}' "$BACKEND_URL/translate")
translated_text=$(echo $translation_response | grep -oP '"translated_text":"\\K[^"]+')

if [ "$translated_text" != "こんにちは" ]; then
  echo "Translation test failed. Response: $translation_response"
  exit 1
fi
echo "Translation test passed."

# Add more tests as needed

echo "E2E tests completed successfully."
