# Load .env file
set dotenv-load := true


######## Local Environment commands ########
lockdeps:
    pip-compile requirements/main
    pip-compile requirements/dev

install:
    pip-sync requirements/dev.txt

sync: lockdeps install

######## General commands ########
start: check_secrets_exist
    APP_PORT=3000 bash start.sh

start_in_socket_mode: check_secrets_exist
    python twisted/socket_app.py

check_secrets_exist:
    #!/usr/bin/env python3
    import os
    envs = [
        'SLACK_BOT_TOKEN', 
        'SLACK_SIGNING_SECRET', 
        'SLACK_APP_TOKEN', 
        'TWIST_OAUTH_TOKEN',
        'GITHUB_TOKEN',
    ]
    for env in envs:
        assert os.getenv(env), f"Missing required {env!r} environment variable"


######## Docker commands ########
build:
    docker build . -t twisted

enter: build
    docker run -it --rm --env-file .env -p 3000:3000 -v $PWD/twisted:/app/twisted -v $HOME/.aws:/root/.aws twisted /bin/bash

runit: build check_secrets_exist
    docker run -it --rm --env-file .env -p 3000:3000 -v $PWD/twisted:/app/twisted -v $HOME/.aws:/root/.aws twisted

