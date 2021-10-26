FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN python3 -m pip install aiofiles jinja2 python-multipart ipaddress

COPY ./app /app

#set user to www-data
USER www-data