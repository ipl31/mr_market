"""
Classes to provide bot skills for FRED API calls.
"""
import logging
import os
from fredapi import Fred
from .ISkill import ISkill

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

HELP_COMMAND = "help"
FRED_SKILL_ID = "fred"
API_KEY = os.environ.get("FRED_API_KEY")


class FREDSkill(ISkill):
    """ FREDSkill is an ISkill impl providing access to FRED API
        data. See https://mortada.net/python-api-for-fred.html for
        examples.
    """
    skill_id = FRED_SKILL_ID
    fred = None

    def __init__(self):
        self.fred = Fred(api_key=API_KEY)


    def get_help(self):
        return "get_gdp $year"

    def execute(self, command, date=None):
        if command != "get_gdp":
            raise Exception
        return self.get_gdp(date)
    
    def get_commands(self):
        return self.get_help()

    def get_gdp(self, date=None):
        if date is None:
            series = self.fred.get_series('GDP')
            return series.tail(1).to_string()
        series = self.fred.get_series('GDP',
                                      observation_start=date,
                                      observation_end=date)
        return series.to_string()
