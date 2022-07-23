from slack_bolt.adapter.socket_mode import SocketModeHandler
from twisted.config import set_config
from twisted.slack_api import create_slack_app



def start_app(config):
    slack_app = create_slack_app(config)
    socket = SocketModeHandler(slack_app, config.SLACK_APP_TOKEN)
    socket.start()

if __name__ == "__main__":
    config = set_config()
    start_app(config)
