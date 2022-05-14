import os

from loguru import logger
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


slack_app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

@slack_app.event("reaction_added")
def handle_app_mentions(body):
    logger.debug(body)

SocketModeHandler(slack_app, os.environ["SLACK_APP_TOKEN"]).start()
