import abc


class ISkill(abc.ABC):

    @property
    @abc.abstractmethod
    def skill_id(self):
        pass

    @abc.abstractmethod
    def execute(self, command, args):
        pass

    @abc.abstractmethod
    def get_help(self):
        pass

    @abc.abstractmethod
    def get_commands(self):
        pass
