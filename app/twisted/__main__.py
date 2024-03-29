import os
from slack_bolt.adapter.socket_mode import SocketModeHandler
from twisted.config import set_config
from twisted.slack_api import create_slack_app
from loguru import logger


def start_app(config):
    slack_app = create_slack_app(config)
    socket = SocketModeHandler(slack_app, config.SLACK_APP_TOKEN)
    socket.start()

if __name__ == "__main__":
    logger.info("Starting app in socket mode")
    config = set_config(production=not os.getenv('DEVELOPMENT'))
    start_app(config)
