FROM python:3

LABEL MAINTAINER="Diego Silva de Salles disalles7@gmail.com"

WORKDIR /var/www
COPY . /var/www

RUN pip3 install  -r requirements.txt
RUN pip3 install  gunicorn 

RUN gunicorn gettingstarted.wsgi --log-file -

EXPOSE 5000
