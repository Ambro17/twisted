from slack_bolt import App
import os

slack_app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)


@slack_app.event("reaction_added")
def handle_app_mentions(body, say, logger):
    logger.info(body)
    say("What's up?")


