FROM php:7.3-apache 

RUN apt update && apt install -y libxml2-dev

RUN docker-php-ext-install simplexml

COPY ./app/ /var/www/html/
COPY ./flag.txt /flag.txt

USER www-data