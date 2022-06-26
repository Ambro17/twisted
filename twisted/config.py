from dataclasses import dataclass
import os
import json
import boto3
from botocore.exceptions import ClientError
from twisted.ttl_cache import lru_cache_with_ttl


@dataclass(frozen=True)
class Config:
    SLACK_SIGNING_SECRET: str
    SLACK_BOT_TOKEN: str
    SLACK_APP_TOKEN: str
    TWIST_OAUTH_TOKEN: str
    GITHUB_TOKEN: str


def get_config(production=True) -> Config:
    if production:
        secrets = get_secret_from_aws(secret_name="twisted-app-secrets", region='us-east-1')
    else:
        secrets = dict(
            SLACK_SIGNING_SECRET=os.environ['SLACK_SIGNING_SECRET'],
            SLACK_BOT_TOKEN=os.environ['SLACK_BOT_TOKEN'],
            SLACK_APP_TOKEN=os.environ['SLACK_APP_TOKEN'],
            TWIST_OAUTH_TOKEN=os.environ['TWIST_OAUTH_TOKEN'],
            GITHUB_TOKEN=os.environ['GITHUB_TOKEN'],
        )

    return Config(**secrets)


@lru_cache_with_ttl(ttl_in_seconds=60 * 60, maxsize=10)
def get_secret_from_aws(secret_name, region) -> dict:
    client = boto3.client(service_name='secretsmanager', region_name=region)
    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise LookupError(e.response['Error']['Code'])

    return json.loads(response['SecretString'])
