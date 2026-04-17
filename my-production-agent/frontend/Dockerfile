FROM nginx:alpine

# Copy static frontend files
COPY ./ /usr/share/nginx/html/

# Copy nginx config and entrypoint
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./entrypoint.sh /entrypoint.sh

# Make entrypoint executable
RUN chmod +x /entrypoint.sh

EXPOSE 80

# Use the custom entrypoint
ENTRYPOINT ["/entrypoint.sh"]
