from slack_bolt.adapter.socket_mode import SocketModeHandler
from twisted.config import SLACK_APP_TOKEN
from twisted.slack_api import slack_app


socket = SocketModeHandler(slack_app, SLACK_APP_TOKEN)
socket.start()
