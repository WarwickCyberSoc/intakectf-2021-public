FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN apt update && apt install -y ncat && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install aiofiles jinja2 python-multipart ipaddress

COPY ./flag.txt /SuperSecureFlagLocationNoOneWouldGuess.txt
COPY ./app /app

USER www-data
