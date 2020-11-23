

class MisterMarketBot:

    skills = {}

    def __init__(self, skills):
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

    def handle_slack_message(self, message):
        message = message.split(' ', 1)[1]
        if not self._is_skill_message(message):
            return "I do not understand your command."
        skill, command, args = self._parse_command(message)
        result = self._run_skill_command(skill, command, args)
        return result
