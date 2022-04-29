FROM python:3.10.2

RUN pip install -U pip wheel setuptools

WORKDIR /app

COPY requirements/ requirements/
RUN pip install -r requirements/main.txt

ENV APP_PORT ${APP_PORT:-3000}

COPY twisted/ twisted/

RUN echo $APP_PORT


CMD uvicorn twisted.server:api --reload --port ${APP_PORT} --host 0.0.0.0
