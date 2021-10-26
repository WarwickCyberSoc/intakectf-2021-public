FROM ubuntu:20.04

RUN mkdir /srv/vuln
COPY flag.txt fork_you /srv/vuln/
RUN chmod -R 755 /srv/vuln

RUN useradd -s /bin/bash wmg
USER wmg
WORKDIR /srv/vuln

EXPOSE 5000

CMD ["/srv/vuln/fork_you"]