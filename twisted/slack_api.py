from loguru import logger
from slack_bolt import App, Say
from twisted.config import SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET
from twisted.twist.client import get_client as get_twist_client
from twisted.github.client import get_client as get_github_client


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


@slack_app.shortcut('create_twist_thread')
def create_twist_thread(ack, body, message, say: Say):
    ack()
    message = body.get('message', {}).get('text')
    if not message:
        logger.debug("Error getting message from this body %s" % body)

    channel = body['channel']['name'] 
    user = body['user']['name']

    client = get_twist_client()
    title = f"{message:30}...  by {user} at #{channel}"

    logger.debug(f"Creating discussion with title {title!r}")

    appendix = "\n_This thread was created automatically by an integration with slack via message shortcuts_"
    thread = client.create_thread(title=title, body=message + appendix)
    say(f"A new twist was created from the message above: {thread}\n"
        "_You're invited to follow the conversation there so everyone can voice their opinions without rush_")

    logger.debug(f"Thread {thread!r} was created and the channel was notified")
