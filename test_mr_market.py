import pytest
from app import app
from app import views


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
    message_block = views.create_message_block(text)
    assert "123abc!" in message_block['text']['text']


def test_post_message_raises():
    with pytest.raises(TypeError):
        channel_id = "foo"
        not_a_list = "not a list"
        views.post_message(channel_id, not_a_list)
