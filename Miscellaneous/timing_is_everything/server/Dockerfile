# sudo docker build -t wmg_ctf_2021_misc_timing_is_everything .
# sudo docker run -d -p 5000:5000 wmg_ctf_2021_misc_timing_is_everything

FROM ubuntu:20.04

RUN apt update && apt install -y socat && rm -rf /var/lib/apt/lists/*

RUN mkdir /srv/timing_is_everything
ADD . /srv/timing_is_everything
RUN chmod -R 755 /srv/timing_is_everything

RUN useradd -s /bin/bash wmg
USER wmg
WORKDIR /srv/timing_is_everything

CMD socat TCP-LISTEN:5000,fork,reuseaddr EXEC:/srv/timing_is_everything/timing_is_everything,stderr
