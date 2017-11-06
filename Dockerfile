FROM python:3.6

WORKDIR /app
VOLUME /app
ADD . /app

RUN cd /app && python setup.py install

CMD 'sh'
