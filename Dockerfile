FROM python:2.7

WORKDIR /app
VOLUME /app
ADD . /app

RUN cd /app && python setup.py install

CMD '/app/test.sh'
