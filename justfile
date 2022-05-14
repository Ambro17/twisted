# Load .env file
set dotenv-load := true

lockdeps:
    pip-compile requirements/main
    pip-compile requirements/dev

install:
    pip-sync requirements/dev.txt

refresh: lockdeps install

build:
    docker build . -t twisted

enter: build
    docker run -it --rm --env-file .env -p 3000:3000 -v $PWD/twisted:/app/twisted twisted /bin/bash 

alias runit := run
run: build check_secrets_exist
    docker run -it --rm --env-file .env -p 3000:3000 -v $PWD/twisted:/app/twisted twisted 

start: check_secrets_exist
    APP_PORT=3000 bash start.sh

check_secrets_exist:
    #!/usr/bin/env python3
    import os
    assert os.getenv('SLACK_BOT_TOKEN'), "Missing required 'SLACK_BOT_TOKEN' environment variable"
    assert os.getenv('SLACK_SIGNING_SECRET'), "Missing required 'SLACK_SIGNING_SECRET' environment variable"
