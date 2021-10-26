FROM python:3.9

# install Selenium & flask
RUN pip install selenium flask

RUN mkdir /app
WORKDIR /app
COPY ./app/ .

EXPOSE 5000
CMD ["/bin/bash", "entrypoint.sh"]