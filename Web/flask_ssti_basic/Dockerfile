FROM python:3.8-slim

RUN pip install flask

COPY ./flask_app /app

WORKDIR /app

USER www-data

ENV FLASK_APP=main.py
ENV FLASK_ENV=production

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]