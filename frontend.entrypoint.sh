#!/bin/sh

# Replace placeholders with environment variables
sed -i 's|apiUrl\s*=\s*"[^"]*"|apiUrl="http://backend:5000/api"|g' /usr/share/nginx/html/main.*.js

# Start Nginx
nginx -g 'daemon off;'