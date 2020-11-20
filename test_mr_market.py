from app import app
from app import helpers
from app.MisterMarketBot import MisterMarketBot


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


skills = {"foo": fooSkill, "bar": barSkill}
bot_id = 'abc123'
bot = MisterMarketBot(skills, bot_id)


def test_MisterMarketBot_is_message_command():
    assert bot._is_message_command("bar") is True
    assert bot._is_message_command("blah") is False


def test_MisterMarketBot_is_payload_from_me():
    assert bot._is_payload_from_me({"user": "123"}) is False
    assert bot._is_payload_from_me({"user": bot_id}) is True


def test_MisterMarketBot_get_skills():
    assert "foo" in bot._get_skills()
    assert "bar" in bot._get_skills()


def test_MisterMarketBot_get_skills_commands():
    assert "get_foo" in bot._get_skill_commands("foo")
    assert "get_bar" in bot._get_skill_commands("bar")
    assert "get_bar_with_param" in bot._get_skill_commands("bar")
    assert "get_foo" not in bot._get_skill_commands("bar")


def test_MisterMarketBot_parse_skill_command():
    skill, command, args = bot._parse_skill_command("bah get_bah param1 param2")
    assert skill == "bah" 
    assert command == "get_bah" 
    assert args == ["param1", "param2"]


def test_MisterMarketBot_run_skill_command():
    result = bot._run_skill_command("foo", "get_foo")
    assert result == "foo"
    result = bot._run_skill_command("bar", "get_bar_with_param",  "baz")
    assert "bar" in result
    assert "baz" in result
