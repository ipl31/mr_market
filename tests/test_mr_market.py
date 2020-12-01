import pytest
from mister_market.MisterMarketBot import MisterMarketBot
from TestSkill import TestSkill


@pytest.fixture
def bot():
    return MisterMarketBot(TestSkill())

def test_is_skill_message(bot):
    assert bot._is_skill_message("test") is True
    assert bot._is_skill_message("blah") is False


def test_get_skills(bot):
    assert "test" in bot._get_skills()


def test_get_skills_commands(bot):
    assert "test_command" in bot._get_skill_commands("test")


def test_parse_command(bot):
    skill, command, args = \
            bot._parse_command("test test_command param1 param2")
    assert skill == "test"
    assert command == "test_command"
    assert args == ["param1", "param2"]


def test_run_skill_command(bot):
    result = bot._run_skill_command("test", "test_command")
    assert "test_execute" in result
    result = bot._run_skill_command("test", "test_command",  "baz")
    assert "baz" in result

def test_handle_slack_message(bot):
    result = bot.handle_slack_message("not a command")
    assert "I do not understand your command" in result

