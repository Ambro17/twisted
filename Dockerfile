FROM python:3.10.2

RUN pip install -U pip wheel setuptools

WORKDIR /app

COPY start.sh start.sh
COPY pyproject.toml pyproject.toml

COPY requirements/ requirements/
RUN pip install -r requirements/main.txt

COPY twisted/ twisted/

ENV APP_PORT ${APP_PORT:-3000}

RUN pip install -e .

RUN echo $APP_PORT

CMD ["python", "twisted/socket_app.py"]