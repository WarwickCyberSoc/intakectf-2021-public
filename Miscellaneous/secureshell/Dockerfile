FROM ubuntu:20.04

RUN apt update && apt install  openssh-server sudo vim -y

# Setup user / shell
RUN mkdir /srv/vuln
COPY shell.py /srv/vuln/shell.py
RUN chmod +x /srv/vuln/shell.py

RUN useradd -s /bin/bash -d /srv/vuln wmg
RUN passwd -d wmg

COPY flag.txt /flag.txt

RUN mkdir -p /run/sshd
COPY sshd_config /etc/ssh/sshd_config

EXPOSE 22

CMD ["/usr/sbin/sshd","-De"]