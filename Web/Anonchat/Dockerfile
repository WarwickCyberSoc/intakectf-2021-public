FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN python3 -m pip install jinja2 requests

COPY ./app /app
COPY ./flag.txt /flag_XBtg7ok5.txt

USER www-data