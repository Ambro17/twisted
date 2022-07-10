FROM python:3.10.2

RUN pip install -U pip wheel setuptools

WORKDIR /app

COPY start.sh start.sh
COPY pyproject.toml pyproject.toml

COPY requirements/ requirements/
RUN pip install -r requirements/main.txt

ENV APP_PORT ${APP_PORT:-3000}

COPY twisted/ twisted/

RUN pip install -e .

CMD ["python", "twisted/socket_app.py"]