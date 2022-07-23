"""This module contains application configuration

Client modules should use it like this

from twisted.config import app_config, set_config, get_config

# Set config
set_config(production=False)  # Will set it from environment variables
set_config()                  # Will set it from aws secrets manager

# Get Config
token = get_config().SLACK_SIGNING_SECRET
"""
from contextvars import ContextVar
from dataclasses import dataclass
import os
import json

import boto3


app_config: ContextVar['Config'] = ContextVar('app_config')


@dataclass(frozen=True)
class Config:
    SLACK_SIGNING_SECRET: str
    SLACK_BOT_TOKEN: str
    SLACK_APP_TOKEN: str
    TWIST_OAUTH_TOKEN: str
    GITHUB_TOKEN: str


def get_config():
    return app_config.get()


def set_config(production=True) -> Config:
    if production:
        client = boto3.client('secretsmanager', region_name='us-east-1') 
        secrets = _read_secrets_from_aws(
            client, 
            'twisted-app-secrets'
        )
    else:
        secrets = dict(
            SLACK_SIGNING_SECRET=os.environ['SLACK_SIGNING_SECRET'],
            SLACK_BOT_TOKEN=os.environ['SLACK_BOT_TOKEN'],
            SLACK_APP_TOKEN=os.environ['SLACK_APP_TOKEN'],
            TWIST_OAUTH_TOKEN=os.environ['TWIST_OAUTH_TOKEN'],
            GITHUB_TOKEN=os.environ['GITHUB_TOKEN'],
        )

    app_config.set(Config(**secrets))

    return app_config.get()


def _read_secrets_from_aws(client, secret_name) -> dict:
    return json.loads(client.get_secret_value(SecretId=secret_name)['SecretString'])
