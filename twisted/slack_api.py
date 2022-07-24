from textwrap import dedent
from loguru import logger
from slack_sdk import WebClient
from slack_bolt import App
from twisted.twist.client import get_client as get_twist_client
from twisted.slack_utils.utils import create_modal, link


def create_slack_app(config):
    slack_app = App(token=config.SLACK_BOT_TOKEN, signing_secret=config.SLACK_SIGNING_SECRET)

    @slack_app.middleware
    def log_request(client, context, payload, next):
        logger.debug(payload)
        next()


    NEW_THREAD_ACTION_ID = 'new_twist_thread'
    CREATE_SHORTCUT_CALLBACK_ID = 'create_twist_thread'

    @slack_app.shortcut(CREATE_SHORTCUT_CALLBACK_ID)
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


    @slack_app.command('/shipping')
    def send_shipping_info(ack, respond):
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
