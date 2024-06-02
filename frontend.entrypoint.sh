#!/bin/sh

# Replace placeholders with environment variables
sed -i 's|apiUrl\s*=\s*"[^"]*"|apiUrl="backend:5000"|g' /usr/share/nginx/html/main.*.js

# Start Nginx
nginx -g 'daemon off;'