FROM python:3.9 AS builder-image

# Setup random data
RUN pip install faker
COPY ./generate_fake_data.py /root/generate_fake_data.py
RUN python3 /root/generate_fake_data.py


FROM nginx:latest as final-image

COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY ./website /usr/share/nginx/html/

COPY --from=builder-image /data.csv /usr/share/nginx/html/download/data.csv