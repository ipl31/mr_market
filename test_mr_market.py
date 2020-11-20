from app import app
from app import helpers
from app.MisterMarketBot import MisterMarketBot
from app.TestSkill import TestSkill


def test_index():
    client = app.test_client()
    response = client.get('/', content_type='html/text')
    assert response.status_code == 200


def test_404():
    client = app.test_client()
    response = client.get('/asdasdasda', content_type='html/text')
    assert response.status_code == 404


def test_create_message_block():
    text = "123abc!"
    message_block = helpers.create_message_block(text)
    assert "123abc!" in message_block['text']['text']


class fooSkill():

    def get_foo():
        return "foo"


class barSkill():

    def get_bar():
        return "bar"

    def get_bar_with_param(param):
        return [param, "bar"]


bot_id = 'abc123'
bot = MisterMarketBot(TestSkill(), bot_id)


def test_MisterMarketBot_is_message_command():
    assert bot._is_skill_message("test") is True
    assert bot._is_skill_message("blah") is False


def test_MisterMarketBot_is_payload_from_me():
    assert bot._is_payload_from_me({"user": "123"}) is False
    assert bot._is_payload_from_me({"user": bot_id}) is True


def test_MisterMarketBot_get_skills():
    assert "test" in bot._get_skills()


def test_MisterMarketBot_get_skills_commands():
    assert "test_command" in bot._get_skill_commands("test")


def test_MisterMarketBot_parse_command():
    skill, command, args = \
            bot._parse_command("test test_command param1 param2")
    assert skill == "test"
    assert command == "test_command"
    assert args == ["param1", "param2"]


def test_MisterMarketBot_run_skill_command():
    result = bot._run_skill_command("test", "test_command")
    assert "test_execute" in result
    result = bot._run_skill_command("test", "test_command",  "baz")
    assert "baz" in result
