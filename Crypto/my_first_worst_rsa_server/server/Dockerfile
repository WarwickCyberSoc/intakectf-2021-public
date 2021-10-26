# sudo docker build -t wmg_ctf_2021_rsa_server .
# sudo docker run -d -p 5000:5000 wmg_ctf_2021_rsa_server

FROM ubuntu:20.04

RUN apt update && apt install -y python3 python3-pip build-essential python3-dev socat && rm -rf /var/lib/apt/lists/*

RUN mkdir /srv/rsa_server
ADD . /srv/rsa_server
RUN chmod -R 755 /srv/rsa_server
RUN python3 -m pip install -r /srv/rsa_server/requirements.txt

RUN useradd -s /bin/bash wmg
USER wmg
WORKDIR /srv/rsa_server

CMD socat TCP-LISTEN:5000,fork,reuseaddr EXEC:"python3 -u /srv/rsa_server/my_first_worst_rsa_server.py",stderr
