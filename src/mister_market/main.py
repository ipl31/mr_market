from .app import app
from .events import * # noqa ignore=F405


def main():
    app.start(port=5000)
