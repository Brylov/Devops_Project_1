#!/bin/bash

# URL of your frontend and backend
FRONTEND_IP=$(docker inspect -f '{{.NetworkSettings.Networks.jenkins_nw.IPAddress}}' frontend_jenkins_test)
BACKEND_IP=$(docker inspect -f '{{.NetworkSettings.Networks.jenkins_nw.IPAddress}}' backend_jenkins_test)
FRONTEND_URL="http://$FRONTEND_IP"
BACKEND_URL="http://$BACKEND_IP:5000/"

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
translated_text=$(echo "$translation_response" | grep -oP '"translated_text":"\\K[^"]+' | python3 -c 'import sys,json; print(json.loads(sys.stdin.read())["translated_text"].encode().decode("unicode-escape"))')
if [ "$translated_text" != "こんにちは" ]; then
  echo "Translation test failed. Response: $translation_response"
  exit 1
fi
echo "Translation test passed."

# Add more tests as needed

echo "E2E tests completed successfully."

