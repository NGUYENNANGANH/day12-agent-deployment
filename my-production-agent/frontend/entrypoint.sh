#!/bin/sh
# Render nginx.conf from template using BACKEND_URL.
# Defaults support local docker-compose (api service) if not set.
export BACKEND_URL="${BACKEND_URL:-http://api:8000}"

envsubst '${BACKEND_URL}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Start Nginx
nginx -g "daemon off;"
