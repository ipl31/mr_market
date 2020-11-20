import os
from .helpers import get_public_methods, post_message
from slack import WebClient

# TODO: Centralize client code in a module
client_token = os.environ.get("SLACK_TOKEN")
slack_client = WebClient(token=client_token)


class MisterMarketBot:

    skills = {}
    bot_id = None

    def __init__(self, skills, bot_id):
        """ skills: {"prefix": object} """
        # TODO: Check we are not overwriting skills
        self.skills.update(skills)
        self.bot_id = bot_id

    def _get_skills(self):
        return list(self.skills.keys())

    def _get_skill_commands(self, skill):
        if skill not in self.skills:
            return None
        return get_public_methods(self.skills[skill])

    def _run_skill_command(self, skill, command, *args):
        if skill not in self._get_skills():
            raise KeyError("Unknown skill")
        method = getattr(self.skills[skill], command)
        result = method(*args)
        return result

    def _is_message_command(self, message):
        maybe_command = message.split()[0]
        if maybe_command in self.skills:
            return True
        return False

    def _is_payload_from_me(self, payload):
        if payload.get("user") == self.bot_id:
            return True
        return False

    def _send_error_message(self, channel_id):
        message = "I did not understand your command."
        post_message(channel_id, message)

    def handle_slack_event(self, payload):
        event = payload.get("event", {})
        if self._is_payload_from_me(event):
            return

        # user_id = payload.get("user")
        channel_id = event.get("channel")
        text = event.get("text")
        message_with_user_stripped = text.split(' ', 1)[1]

        if not self._is_message_command(message_with_user_stripped):
            self._send_error_message(channel_id)
            return
        tokenized_command = message_with_user_stripped.split()
        skill = tokenized_command.pop()
        command = tokenized_command.pop()
        args = tokenized_command
        self._run_skill_command(skill, command, args)
