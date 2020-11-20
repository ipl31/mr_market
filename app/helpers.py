import os
from slack import WebClient

client_token = os.environ.get("SLACK_TOKEN")
slack_client = WebClient(token=client_token)


def create_message_block(text):
    msg_block = {
                "type": "section",
                "text": {"type": "mrkdwn", "text": (f"{text}\n\n"),
                         },
                }
    return msg_block


def post_message(channel_id, text):
    block = create_message_block(text)
    message = {"channel": channel_id,
               "blocks": [block],
               }
    slack_client.chat_postMessage(**message)


def get_public_methods(object):
    methods = []
    for method_name in dir(object):
        if method_name.startswith("__"):
            continue
        if method_name.startswith("_"):
            continue
        if callable(getattr(object, method_name)):
            methods.append(str(method_name))
    return methods
