from slack_bolt.adapter.socket_mode import SocketModeHandler
from twisted.config import get_config
from twisted.slack_api import create_slack_app



def start_app():
    config = get_config()
    slack_app = create_slack_app()
    socket = SocketModeHandler(slack_app, config.SLACK_APP_TOKEN)
    socket.start()

if __name__ == "__main__":
    start_app()
