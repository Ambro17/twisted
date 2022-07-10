from loguru import logger
from slack_sdk import WebClient
from slack_bolt import App, Say
from twisted.twist.client import get_client as get_twist_client
from twisted.github.client import get_client as get_github_client
from twisted.slack_utils.utils import create_modal


def create_slack_app(config):
    slack_app = App(token=config.SLACK_BOT_TOKEN, signing_secret=config.SLACK_SIGNING_SECRET)

    NEW_THREAD_ACTION_ID = 'new_twist_thread'


    @slack_app.shortcut('create_twist_thread')
    def show_twist_thread_modal(ack, body, message, client: WebClient):
        """Open a modal (popup) with prefilled information to create a new thread"""
        ack()
        logger.debug(body)
        message = body.get('message', {}).get('text')
        if not message:
            logger.debug("Error getting message from this body %s" % body)

        # Show new thread modal
        modal = create_modal(title=message[:140], body=message, action_id=NEW_THREAD_ACTION_ID)
        client.views_open(
            trigger_id=body['trigger_id'],
            view=modal
        )


    @slack_app.view(NEW_THREAD_ACTION_ID)
    def create_twist_thread(ack, body, client: WebClient):
        """Create a twist thread based on what was submitted on the create twist message"""
        ack()
        logger.debug(body)

        user = body['user']['name']
        user_id = body['user']['id']
        response = body['view']['state']['values']
        title = response['block_title']['thread_title_action_id']['value']
        description = response['block_body']['thread_description_action_id']['value']

        twist = get_twist_client(config)
        
        footer = f"\n\n_This thread was created through a slack shortcut integration by {user}_"
        thread = twist.create_thread(title=title, body=description + footer)
        logger.debug(f"Thread {thread!r} was created and the channel was notified")
        client.chat_postEphemeral(
            channel=user_id,
            user=user_id,
            text=f'✅ Your thread was created here {thread}'
        )


    return slack_app
