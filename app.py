import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))


def render_message(channel, msg):
    return {
        "channel": channel,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"{msg}\n\n"
                    ),
                },
            },
        ],
    }


def post_message(msg):
    slack_web_client.chat_postMessage(**msg)


@slack_events_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    text = event.get("text")
    channel_id = event.get("channel")

    # hard-coded part to simulate interaction
    if "hi, boxxy" in text.lower():
        return post_message(render_message(channel_id, "Hi, how can I help you?"))


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(host='0.0.0.0', port=3000)
