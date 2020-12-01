import pytest
from mister_market import iex_skills


@pytest.fixture
def skill():
    return iex_skills.IexStockSkill() 

def test_skill_id(skill):
    assert iex_skills.IEX_STOCK_SKILL_ID in skill.skill_id

def test_help_in_commands(skill):
    assert iex_skills.HELP_COMMAND in skill.get_commands()

def test_iex_methods_in_commands(skill):
    assert "get_price" in skill.get_commands()
    assert "get_balance_sheet" in skill.get_commands()

# Requires test token and IEX test endpoint are configured
# in environment.
def test_get_price(skill):
    price = skill.execute("get_price", ['AAPL'])
    # TODO: This is a lame test.
    assert isinstance(price, str) is True
