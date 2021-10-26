FROM php:7.2-apache 

RUN pecl install redis-5.3.4 \
    && pecl install xdebug-2.8.1 \
    && docker-php-ext-enable redis xdebug

RUN apt update && apt install -y build-essential wget curl gnupg supervisor sudo cron netcat

# Install latest chrome dev package and fonts to support major charsets (Chinese, Japanese, Arabic, Hebrew, Thai and a few others)
# Note: this installs the necessary libs to make the bundled version of Chromium that Puppeteer
# installs, work.
RUN apt-get update \
    && apt-get install -y wget gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true

# Install Node
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash \
    && apt-get install nodejs -yq

# Setup Redis
RUN adduser --system --group --no-create-home redis \
    && mkdir /var/lib/redis \
    && chown redis:redis /var/lib/redis \
    && chmod 770 /var/lib/redis \
    && mkdir /etc/redis

RUN cd /root \
    && wget https://download.redis.io/releases/redis-3.2.5.tar.gz \
    && tar xzf redis-3.2.5.tar.gz  \ 
    && cd redis-3.2.5  \
    && make \
    && cp src/redis-server /usr/bin/redis-server \
    && cp redis.conf /etc/redis/

# Setup Bot
RUN mkdir /opt/bot \
    && chown root:root /opt/bot \
    && chmod 770 /opt/bot 

COPY ./supervisor.conf /etc/supervisord.conf

COPY ./bot/ /opt/bot/
RUN cd /opt/bot && npm ci

# Setup docker entrypoint
COPY ./docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh

# Copy files in
COPY ./html/ /var/www/html/

# hey, i'm sure this can't go wrong!
RUN chown root:root /var/www/html
RUN chmod -R 555 /var/www/html
RUN mkdir /var/www/html/redis
RUN chown root:redis /var/www/html/redis
RUN chmod 575 /var/www/html/redis

# Copy the flag with a random name
COPY ./flag.txt /flag.txt
RUN mv /flag.txt /flag_$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 15 | head -n 1).txt


###
### Setup cronjob for maintaining challenge health
###

# Copy hello-cron file to the cron.d directory
COPY ./reset-cron /etc/cron.d/reset-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/reset-cron

# Apply cron job
RUN crontab /etc/cron.d/reset-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

COPY ./cleanup.sh /root/cleanup.sh
RUN chmod +x /root/cleanup.sh
###
###
###

EXPOSE 80

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["apache2-foreground"]