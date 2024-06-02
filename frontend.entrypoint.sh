#!/bin/sh

# Replace placeholders with environment variables
sed -i "s|apiUrl\s*=\s*\"[^\"]*\"|apiUrl=\"$API_URL\"|g" /usr/share/nginx/html/main.*.js

# Start Nginx
nginx -g 'daemon off;'