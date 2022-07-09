from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Config:
    SLACK_SIGNING_SECRET: str
    SLACK_BOT_TOKEN: str
    SLACK_APP_TOKEN: str
    TWIST_OAUTH_TOKEN: str
    GITHUB_TOKEN: str
    AWS_AMAZON_KEY: str
    AWS_AMAZON_SECRET: str


def get_config(production=True) -> Config:
    secrets = dict(
        SLACK_SIGNING_SECRET=os.environ['SLACK_SIGNING_SECRET'],
        SLACK_BOT_TOKEN=os.environ['SLACK_BOT_TOKEN'],
        SLACK_APP_TOKEN=os.environ['SLACK_APP_TOKEN'],
        TWIST_OAUTH_TOKEN=os.environ['TWIST_OAUTH_TOKEN'],
        GITHUB_TOKEN=os.environ['GITHUB_TOKEN'],
        AWS_AMAZON_KEY=os.environ['AWS_AMAZON_KEY'],
        AWS_AMAZON_SECRET=os.environ['AWS_AMAZON_SECRET'],
    )
    return Config(**secrets)

