# sudo docker build -t wmg_ctf_2021_crypto_lottery .
# sudo docker run -d -p 5000:5000 wmg_ctf_2021_crypto_lottery

FROM ubuntu:20.04

RUN apt update && apt install -y python3 socat && rm -rf /var/lib/apt/lists/*

RUN mkdir /srv/lottery
ADD . /srv/lottery
RUN chmod -R 755 /srv/lottery

RUN useradd -s /bin/bash wmg
USER wmg
WORKDIR /srv/lottery

CMD socat TCP-LISTEN:5000,fork,reuseaddr EXEC:"python3 -u /srv/lottery/lottery.py",stderr
