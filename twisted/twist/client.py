"""Twist client that allows to open new threads"""
import requests

from twisted.config import TWIST_OAUTH_TOKEN


class TwistClient:

    def __init__(self, token, channel=568598) -> None:
        self.token = token
        self.channel = channel

    def login(self, username, password):
        resp = requests.post(
            'https://api.twist.com/api/v3/users/login',
            json=dict(email=username, password=password)
        )
        body = resp.json()
        self.token = body['token']
        return self.token

    def create_thread(self, title, body, channel_id=None, send_as_integration=True):
        resp = requests.post(
            'https://api.twist.com/api/v3/threads/add',
            json=dict(
                channel_id=channel_id or self.channel,
                title=title,
                content=body,
                send_as_integration=send_as_integration,   # REQUIRES app oauth token. Comment out if you've a personal token!!!
            ),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        return resp.json()



cli = TwistClient(TWIST_OAUTH_TOKEN)
b = cli.create_thread('This was created automatically', 'and this too')
print(b)
