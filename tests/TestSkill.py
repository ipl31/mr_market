from mister_market.ISkill import ISkill


class TestSkill(ISkill):

    __test__ = False

    def __init__(self):
        pass

    @property
    def skill_id(self):
        return "test"

    def execute(self, command, *args):
        return ["test_execute", *args]

    def get_help(self):
        return "test_help"

    def get_commands(self):
        return ["test_command"]
