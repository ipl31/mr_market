import pytest
from mister_market.helpers import get_public_methods


@pytest.fixture
def dummy_object():
    class foo:

        def __init__(self):
            pass

        def _private_foo(self):
            pass

        def public_foo(self):
            pass

    return foo()


def test_get_public_methods(dummy_object):
    assert "public_foo" in get_public_methods(dummy_object)
    assert "__init__" not in get_public_methods(dummy_object)
    assert "_private_foo" not in get_public_methods(dummy_object)
