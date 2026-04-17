FROM nginx:alpine

# Copy ALL content from static folder directly to web root
COPY ./static/ /usr/share/nginx/html/

# Delete default nginx config that causes the "Welcome to nginx" page
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config and entrypoint
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./entrypoint.sh /entrypoint.sh

# Make entrypoint executable
RUN chmod +x /entrypoint.sh

EXPOSE 80

# Use the custom entrypoint
ENTRYPOINT ["/entrypoint.sh"]
