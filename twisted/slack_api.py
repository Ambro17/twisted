from loguru import logger
from slack_bolt import App
from twisted.config import SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET


slack_app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)


@slack_app.event("reaction_added")
def handle_app_mentions(body):
    logger.debug(body)
