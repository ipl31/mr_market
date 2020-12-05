import pytest
from mister_market.slack import BlockBuilder, MessageBuilder


@pytest.fixture
def block_builder() -> BlockBuilder:
    return BlockBuilder()


@pytest.fixture
def message_builder() -> MessageBuilder:
    return MessageBuilder()


def test_message_builder(message_builder):
    message_builder.add_text(" foo ")
    message_builder.add_bold_text("bar")
    message_builder.add_terminal_text("foobar")
    product = message_builder.product
    assert " foo " in product
    assert "*bar*" in product
    assert "`foobar`" in product
    assert len(message_builder.product) == 0


def test_block_builder(block_builder, message_builder):
    message_builder.add_text("bar")
    block_builder.add_header_block(message_builder.product)
    message_builder.add_text("foo")
    block_builder.add_section_block(message_builder.product)
    block_builder.add_divider_block()
    product = block_builder.product
    assert len(block_builder.product) == 0
    assert len(product) == 3
    assert "bar" in product[0].text.text
    assert "foo" in product[1].text.text
