from app import app


def test_index():
    client = app.test_client()
    response = client.get('/', content_type='html/text')
    assert response.status_code == 200


def test_404():
    client = app.test_client()
    response = client.get('/asdasdasda', content_type='html/text')
    assert response.status_code == 404
