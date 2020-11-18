import logging
from flask import Flask

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.logger.debug("Starting Mr. Market Flask App")

# TODO: Use Blueprints
from .views import *
