FROM ubuntu:20.04

RUN apt update && apt install -y socat python3 && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
COPY ./server.py /app

RUN chmod +x /app/server.py

RUN useradd -s /bin/bash wmg
USER wmg
WORKDIR /app

EXPOSE 5000
CMD socat TCP-LISTEN:5000,fork,reuseaddr EXEC:/app/server.py,stderr