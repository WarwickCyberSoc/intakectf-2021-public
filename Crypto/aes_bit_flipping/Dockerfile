# sudo docker build -t wmg_ctf_2021_aes_bitflip .
# sudo docker run -d -p 5000:5000 wmg_ctf_2021_aes_bitflip

FROM ubuntu:20.04

RUN apt update && apt install -y socat python3 python3-pip && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install pycryptodome

RUN mkdir /app
COPY ./app /app
RUN chmod +x /app/the_nice_robot.py

RUN useradd -s /bin/bash wmg
USER wmg
WORKDIR /app

EXPOSE 5000
CMD socat TCP-LISTEN:5000,fork,reuseaddr EXEC:/app/the_nice_robot.py,stderr
