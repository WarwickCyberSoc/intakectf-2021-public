# sudo docker build -t wmg_ctf_2021_pwn_bof_6 .
# sudo docker run -d -p 42006:42006 wmg_ctf_2021_pwn_bof_6

FROM ubuntu:20.04

RUN apt update && apt install -y socat && rm -rf /var/lib/apt/lists/*

RUN mkdir /srv/vuln
ADD . /srv/vuln
RUN chmod -R 755 /srv/vuln

RUN useradd -s /bin/bash wmg
USER wmg
WORKDIR /srv/vuln

CMD socat TCP-LISTEN:42006,fork,reuseaddr EXEC:/srv/vuln/vuln,stderr
