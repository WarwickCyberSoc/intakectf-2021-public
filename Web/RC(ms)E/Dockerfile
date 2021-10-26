FROM php:7.3-apache 

RUN docker-php-ext-install mysqli pdo_mysql

RUN apt update && apt install -y netcat ncat && rm -rf /var/lib/apt/lists/*

WORKDIR /

COPY ./app/html /var/www/html
RUN chmod -R 655 /var/www
RUN chmod -R 775 /var/www/html/uploadImage/
RUN chown -R root:www-data /var/www
RUN useradd -p '$6$fTMNmaqQA$eJxMGmY1K2m7z4CgeYpBYlm3KGtdNE55mVt6wnu3O3dsfiDmKDDvopaZ1pYjrV4F1STagtgu.6EOhXNovyX8U/' examiner
COPY flag.txt /home/examiner/flag.txt
RUN chown root:root /home/examiner/flag.txt
RUN chmod 444 /home/examiner/flag.txt