#!/bin/sh
# Get the first nameserver from resolv.conf
NAMESERVER=$(grep nameserver /etc/resolv.conf | head -n 1 | awk '{print $2}')
# Replace the placeholder in the config
sed -i "s/DNS_RESOLVER_PLACEHOLDER/$NAMESERVER/g" /etc/nginx/nginx.conf
# Start Nginx
nginx -g "daemon off;"
