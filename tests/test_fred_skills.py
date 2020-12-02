import pytest
from mister_market import fred_skills


@pytest.fixture
def skill():
    skill = fred_skills.FREDSkill()
    return skill

def test_get_gdp(skill):
    gdp = skill.get_gdp()
    date, value = gdp.split()
    assert "2020" in date
