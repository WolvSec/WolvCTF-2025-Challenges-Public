FROM php:8.4-apache

# Install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copy the index page
COPY index.php /var/www/html/index.php

# Create the uploads directory and make it unreadable but writeable
RUN mkdir -p /var/www/html/uploads && \
    chown root:www-data /var/www/html/uploads && \
    chmod 730 /var/www/html/uploads

# Make /var/www/html/ only readable
RUN chown root:www-data /var/www/html/ && \
    chmod 750 /var/www/html/

# Copy flag.txt over
COPY flag.txt /var/www/html/flag.txt
RUN chown root:root /var/www/html/flag.txt && \
    chmod 400 /var/www/html/flag.txt

# Copy get_flag over and compile
COPY get_flag.c /var/www/html/get_flag.c
RUN gcc /var/www/html/get_flag.c -o /var/www/html/get_flag && \
    chown root:www-data /var/www/html/get_flag && \
    chmod 4755 /var/www/html/get_flag && \
    rm /var/www/html/get_flag.c

# Create a cron job to delete uploads every hour, we can review them fast enough
RUN echo "0 * * * * root find /var/www/html/uploads -type f -delete" > /etc/cron.d/delete-uploads

RUN chmod 0644 /etc/cron.d/delete-uploads

RUN crontab /etc/cron.d/delete-uploads

# Start apache and cron
CMD bash -c "cron && apache2-foreground"
