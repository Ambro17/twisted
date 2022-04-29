# Load .env file
set dotenv-load := true

lockdeps:
    python3 -m pip-compile requirements/main
    python3 -m pip-compile requirements/dev

install:
    pip-sync requirements/dev.txt

build:
    docker build . -t twisted

enter: build
    docker run -it --rm --env-file .env -p 3000:3000 twisted /bin/bash 

alias runit := run
run: build check_secrets_exist
    docker run -it --rm --env-file .env -p 3000:3000 twisted 

start: check_secrets_exist
    APP_PORT=3000 bash start.sh

check_secrets_exist:
    #!/usr/bin/env python3
    import os
    assert os.getenv('SLACK_BOT_TOKEN'), "Missing required 'SLACK_BOT_TOKEN' environment variable"
    assert os.getenv('SLACK_SIGNING_SECRET'), "Missing required 'SLACK_SIGNING_SECRET' environment variable"
