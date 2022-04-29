FROM python:3.10.2

RUN pip install -U pip wheel setuptools

WORKDIR /app

COPY start.sh start.sh

COPY requirements/ requirements/
RUN pip install -r requirements/main.txt

ENV APP_PORT ${APP_PORT:-3000}

COPY twisted/ twisted/

RUN echo $APP_PORT


CMD ["/bin/bash", "start.sh"]