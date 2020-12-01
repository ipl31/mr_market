import pytest
from mister_market import iex_skills
from iexfinance.utils.exceptions import IEXQueryError


@pytest.fixture
def skill():
    skill = iex_skills.IexStockSkill()
    return skill


def test_skill_id(skill):
    assert iex_skills.IEX_STOCK_SKILL_ID in skill.skill_id


def test_help_in_commands(skill):
    assert iex_skills.HELP_COMMAND in skill.get_commands()


def test_help_command(skill):
    help_result = skill.execute("help")
    assert isinstance(help_result, str)
    assert "get_price" in help_result


def test_iex_methods_in_commands(skill):
    assert "get_price" in skill.get_commands()
    assert "get_balance_sheet" in skill.get_commands()


# Requires test token and IEX test endpoint are configured
# in environment.
def test_get_price(skill):
    price = skill.execute("get_price", ['AAPL'])
    # TODO: This is a lame test.
    assert isinstance(price, str) is True


def test_bad_symbol_raises(skill):
    bad_symbol = "asdasdasdasdadas"
    with pytest.raises(IEXQueryError):
        skill._execute("get_price", [bad_symbol])


def test_bad_symbol_error_msg(skill):
    bad_symbol = "asdasdasdasdadas"
    assert "check symbol" in skill.execute("get_price",
                                           [bad_symbol])
