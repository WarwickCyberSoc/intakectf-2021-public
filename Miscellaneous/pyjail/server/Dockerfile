# sudo docker build -t intake_ctf_pyjail .
# sudo docker run -d --rm -p 5000:5000 intake_ctf_pyjail

FROM ubuntu:20.04

RUN apt update && apt install -y socat python3 && rm -rf /var/lib/apt/lists/*

RUN mkdir /srv/vuln
ADD . /srv/vuln
RUN chmod -R 755 /srv/vuln

RUN useradd -s /bin/bash wmg
USER wmg
WORKDIR /srv/vuln

CMD socat TCP-LISTEN:5000,fork,reuseaddr EXEC:'/usr/bin/python3 -u /srv/vuln/shell.py',stderr
