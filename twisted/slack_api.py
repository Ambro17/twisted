from loguru import logger
from slack_bolt import App, Say
from twisted.config import SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET


slack_app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)


@slack_app.event("reaction_added")
def handle_app_mentions(event, body, say: Say):
    """When a reaction is added, do something"""
    logger.debug(body)
    reaction = event['reaction']
    if reaction == 'github':
        say('Hey, you reacted with github emoji :github:')
    elif reaction == 'twist2':
        say('Hey, you reacted with twist emoji :twist2:')
