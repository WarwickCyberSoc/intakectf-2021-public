# sudo docker build -t regex101 .
# sudo docker run -d -p 5000:5000 regex101

FROM ubuntu:20.04

RUN apt update && apt install -y socat && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
COPY ./target/release/regex101 /app
COPY ./flag.txt /app
RUN chmod +x /app/regex101
RUN chmod 444 /app/flag.txt

RUN useradd -s /bin/bash wmg
USER wmg
WORKDIR /app

EXPOSE 5000
CMD socat TCP-LISTEN:5000,fork,reuseaddr EXEC:/app/regex101,stderr