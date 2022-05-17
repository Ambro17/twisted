"""This module is responsible of handling interaction via HTTP against the world

No other module should know that the bot is exposing its funcionality over the web.
It works by translating a fastapi request into something bolt framework can work on
After bolt returns a response, it transforms it back to a fastapi response.
This design allows to change the web framework as it is uncoupled from app logic.
"""
from fastapi import FastAPI, Request
from slack_bolt.adapter.fastapi import SlackRequestHandler as SlackToFastApiAdapter
from twisted.slack_api import slack_app


def create_app():
    request_handler = SlackToFastApiAdapter(slack_app)
    api = FastAPI()


    @api.get("/")
    def home():
        return {'ok': True}


    @api.post("/slack/events")
    async def endpoint(req: Request):
        return await request_handler.handle(req)


    return api