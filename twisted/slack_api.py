import os

from loguru import logger
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from twisted.config import SLACK_APP_TOKEN, SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET


slack_app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

@slack_app.event("reaction_added")
def handle_app_mentions(body):
    logger.debug(body)

socket = SocketModeHandler(slack_app, SLACK_APP_TOKEN)
# socket.start()
