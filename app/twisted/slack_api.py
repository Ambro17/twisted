from textwrap import dedent
from loguru import logger
from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.context import BoltContext
from traceback import format_exception
from twisted.twist.client import get_client as get_twist_client
from twisted.slack_utils.utils import create_modal, link


def create_slack_app(config):
    slack_app = App(token=config.SLACK_BOT_TOKEN, signing_secret=config.SLACK_SIGNING_SECRET)

    # Just to test scaling on memory usage
    memory_leak = []

    @slack_app.error
    def error_handler(context: BoltContext, payload: dict, error: Exception):
        traceback = '\n'.join(format_exception(error))
        logger.error(f"🤕 An unexpected error happened when handling {payload=}\nError:\n{traceback}")
        context.ack()
        message = f"🤕 Something went wrong, can you please retry later?\n`{repr(error)}`"

        # Best effort to notify user
        try:
            context.respond(message)
        except Exception:
            try:
                context.say(message)
            except Exception:
                logger.error("Could not notify user of the error")


    @slack_app.middleware
    def log_slack_request_payload(payload, next):
        logger.debug(payload)
        next()


    NEW_THREAD_ACTION_ID = 'new_twist_thread'
    CREATE_SHORTCUT_CALLBACK_ID = 'create_twist_thread'

    @slack_app.shortcut(CREATE_SHORTCUT_CALLBACK_ID)
    def create_twist_thread_modal(ack, body, message, client: WebClient):
        """Open a modal (popup) with prefilled information to create a new thread"""
        ack()
        message = body.get('message', {}).get('text')
        if not message:
            logger.debug("Error getting message from this body %s" % body)

        channel_id = body['channel']['id']
        timestamp = body['message_ts']
        message_permalink = client.chat_getPermalink(channel=channel_id, message_ts=timestamp)

        # Show modal to create thread with prefilled title and body
        modal = create_modal(
            title=message[:140], 
            body=message, 
            action_id=NEW_THREAD_ACTION_ID,
            channel_id=channel_id,
            message_timestamp=timestamp,
            message_permalink=message_permalink['permalink'],
        )
        client.views_open(
            trigger_id=body['trigger_id'],
            view=modal
        )


    @slack_app.view(NEW_THREAD_ACTION_ID)
    def on_submit_create_thread(ack, body, client: WebClient):
        """Create a twist thread based on what was submitted on the create twist message"""
        ack()

        user = body['user']['name']
        channel_id, message_ts, message_link = body['view']['private_metadata'].split('|')
        response = body['view']['state']['values']
        title = response['block_title']['thread_title_action_id']['value']
        description = response['block_body']['thread_description_action_id']['value']

        twist = get_twist_client(config)
        
        # Add link to original message in thread!
        footer = f"\n\n_This thread was created by {user} from this slack message {message_link} via `@Hero`'s message shortcut_"
        thread = twist.create_thread(title=title, body=description + footer)
        logger.debug(f"Thread {thread!r} was created and the channel was notified")

        client.chat_postMessage(
            channel=channel_id,
            thread_ts=message_ts,  # This creates a thread reply from the referenced message
            text=f'✅ A twist thread was created to continue this conversation asynchronously at: {thread} :coffee:'
        )


    @slack_app.command('/shipping')
    def send_shipping_info(ack, respond):
        memory_leak.append(bytearray(256_000_000))
        ack()
        MESSAGE = dedent(
        f"""\
        *Shipping Info*

        :cloudwatch: *Logs | AWS Account*
        {link('Production', 'https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:logs-insights$3FqueryDetail$3D$257E$2528end$257E0$257Estart$257E-3600$257EtimeType$257E$2527RELATIVE$257Eunit$257E$2527seconds$257EeditorString$257E$2527fields*20*40timestamp*0a*7c*20sort*20*40timestamp*20asc*0a*7c*20filter*20*40message*20like*20*27message*27*0a*7c*20parse*20*27*22event*22*3a*20*22*2a*22*27*20as*20event*0a*7c*20parse*20*27*22request_id*22*3a*20*22*2a*22*27*20as*20request_id*20*0a*7c*20parse*20*27*22trace_id*22*3a*20*22*2a*22*27*20as*20trace_id*20*0a*7c*20parse*20*27*3a*20*2a*27*20as*20full_message*20*0a*7c*20fields*20*40timestamp*2c*20*40logStream$257EisLiveTail$257Efalse$257EqueryId$257E$252769c59562-0a77-4566-a48b-16cf929eb382$257Esource$257E$2528$257E$2527*2fecs*2fshiphero-prod-shipping-api$2529$2529')} | Aaron/LLC
        {link('Staging', 'https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:logs-insights$3FqueryDetail$3D$257E$2528end$257E0$257Estart$257E-3600$257EtimeType$257E$2527RELATIVE$257Eunit$257E$2527seconds$257EeditorString$257E$2527fields*20*40timestamp*0a*7c*20sort*20*40timestamp*20asc*0a*7c*20filter*20*40message*20like*20*27message*27*0a*7c*20parse*20*27*22event*22*3a*20*22*2a*22*27*20as*20event*0a*7c*20parse*20*27*22request_id*22*3a*20*22*2a*22*27*20as*20request_id*20*0a*7c*20parse*20*27*22trace_id*22*3a*20*22*2a*22*27*20as*20trace_id*20*0a*7c*20parse*20*27*3a*20*2a*27*20as*20full_message*20*0a*7c*20fields*20*40timestamp*2c*20*40logStream$257EisLiveTail$257Efalse$257EqueryId$257E$252775e66076-1a52-4068-a4f3-90e16a6b8fbc$257Esource$257E$2528$257E$2527*2faws*2fecs*2fstg-shipping-api*2fcontainer-logs$2529$2529')}       | shiphero-stg
        {link('Development', 'https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:logs-insights$3FqueryDetail$3D$257E$2528end$257E0$257Estart$257E-3600$257EtimeType$257E$2527RELATIVE$257Eunit$257E$2527seconds$257EeditorString$257E$2527fields*20*40timestamp*0a*7c*20sort*20*40timestamp*20asc*0a*7c*20filter*20*40message*20like*20*27message*27*0a*7c*20parse*20*27*22event*22*3a*20*22*2a*22*27*20as*20event*0a*7c*20parse*20*27*22request_id*22*3a*20*22*2a*22*27*20as*20request_id*20*0a*7c*20parse*20*27*22trace_id*22*3a*20*22*2a*22*27*20as*20trace_id*20*0a*7c*20parse*20*27*3a*20*2a*27*20as*20full_message*20*0a*7c*20fields*20*40timestamp*2c*20*40logStream$257EisLiveTail$257Efalse$257EqueryId$257E$2527efa5646f-4182-4aa9-b8b0-ede8b2558427$257Esource$257E$2528$257E$2527*2faws*2fecs*2fdev-shipping-api*2fcontainer-logs$2529$2529')} | shiphero-dev


        :aws: *ECS Clusters | AWS Account*
        {link('Production', 'https://us-east-1.console.aws.amazon.com/ecs/home?region=us-east-1#/clusters/shiphero-prod-shipping-api/services')}     | Aaron/LLC
        {link('Staging', 'https://us-east-1.console.aws.amazon.com/ecs/home?region=us-east-1#/clusters/stg-shipping-api/services')}           | shiphero-stg
        {link('Development', 'https://us-east-1.console.aws.amazon.com/ecs/home?region=us-east-1#/clusters/dev-shipping-api/services')} | shiphero-dev


        :github: *Deployment info*
        ```
        Env         | Branch                     | Merge Type       | Deploy Trigger
        Production  | _prod/servers/shipping-api | Merge Commit     | CodePipeline, when triggered
        Staging     | master                     | Squash and Merge | CodePipeline, on merge
        Development | _dev/servers/shipping-api  | Your choice      | Github Action, on merge
        ```


        :rocket: {link('Deploy Prod', 'https://us-east-1.console.aws.amazon.com/codesuite/codepipeline/pipelines/shiphero-prod-shipping-api-deployment/view?region=us-east-1')}
        :sentry: {link('Sentry', 'https://sentry.io/organizations/shiphero-0x/dashboard/12322/?environment=prod&project=5597506&statsPeriod=1h')}
        :honey_pot: {link('Honeycomb', 'https://ui.honeycomb.io/shiphero/datasets/shiphero-core/result/DfoiKjFRAa4?tab=traces')} 
        
        """)
        respond(MESSAGE)


    return slack_app
