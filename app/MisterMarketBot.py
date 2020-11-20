import os
import logging
from slack import WebClient
from .helpers import post_message


logger = logging.getLogger(__name__)
# TODO: Centralize client code in a module
client_token = os.environ.get("SLACK_TOKEN")
slack_client = WebClient(token=client_token)


class MisterMarketBot:

    skills = {}
    bot_id = None

    def __init__(self, skills, bot_id):
        self.bot_id = bot_id

        if isinstance(skills, list):
            for skill in skills:
                new_skill = {skill.skill_id: skill}
                self.skills.update(new_skill)
            return

        new_skill = {skills.skill_id: skills}
        self.skills.update(new_skill)

    def _get_skills(self):
        return self.skills

    def _get_skill_commands(self, skill):
        if skill not in self.skills:
            return None
        return self.skills[skill].get_commands()

    def _parse_command(self, command_string):
        command_list = command_string.split()
        skill = command_list.pop(0)
        command = command_list.pop(0)
        args = command_list
        return skill, command, args

    def _run_skill_command(self, skill, command, *args):
        if skill not in self._get_skills():
            raise KeyError(f"Unknown skill {skill}")
        return self.skills[skill].execute(command, *args)

    def _is_skill_message(self, message):
        maybe_skill = message.split()[0]
        if maybe_skill in self.skills:
            return True
        return False

    def _is_payload_from_me(self, payload):
        if payload.get("user") == self.bot_id:
            return True
        return False

    def _send_error_message(self, channel_id):
        message = "*Sorry!* I did not understand your command."
        post_message(channel_id, message)

    def _send_message(self, channel_id, message):
        post_message(channel_id, message)

    def handle_slack_event(self, payload):
        event = payload.get("event", {})
        if self._is_payload_from_me(event):
            return

        # user_id = payload.get("user")
        channel_id = event.get("channel")
        text = event.get("text")
        logger.debug(f"message text: {text}")
        # strip @user from message
        message = text.split(' ', 1)[1]
        logger.debug(f"message: {message}")

        if not self._is_skill_message(message):
            self._send_error_message(channel_id)
            return
        skill, command, args = self._parse_command(message)
        logger.debug(f"tokenized command: {skill} {command} {args}")
        result = self._run_skill_command(skill, command, args)
        self._send_message(channel_id, result)
