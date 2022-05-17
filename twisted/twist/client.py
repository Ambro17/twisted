"""Twist client that allows to open new threads"""
import requests

from twisted.config import TWIST_OAUTH_TOKEN


class TwistClient:
    WORKSPACE_ID = '34022'

    def __init__(self, token, channel=568598) -> None:
        self.token = token
        self.channel = channel

    def create_thread(self, title, body, channel_id=None, send_as_integration=True) -> str:
        """Create a thread and return its url"""
        resp = requests.post(
            'https://api.twist.com/api/v3/threads/add',
            json=dict(
                channel_id=channel_id or self.channel,
                title=title,
                content=body,
                send_as_integration=send_as_integration,
            ),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        body = resp.json()
        return f"https://twist.com/a/{self.WORKSPACE_ID}/ch/{self.channel}/t/{body['id']}/"

    def delete_thread(self, thread_id) -> None:
        """Delete thread or raise an exception"""
        resp = requests.post(
            'https://api.twist.com/api/v3/threads/remove',
            json={'id': thread_id},
            headers={'Authorization': f'Bearer {self.token}'}
        )
        assert resp.status_code == 200, resp.content


def get_client(token=TWIST_OAUTH_TOKEN):
    return TwistClient(token)
