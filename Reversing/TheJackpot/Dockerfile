# sudo docker build -t wmg_ctf_2021_pwn_bof_1 .
# sudo docker run -d -p 42001:42001 wmg_ctf_2021_pwn_bof_1

FROM ubuntu:20.04

RUN apt update && apt install -y socat python3 && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
COPY ./app /app
RUN chmod +x /app/jackpot.py

RUN useradd -s /bin/bash wmg
USER wmg
WORKDIR /app

EXPOSE 5000
CMD socat TCP-LISTEN:5000,fork,reuseaddr EXEC:/app/jackpot.py,stderr
