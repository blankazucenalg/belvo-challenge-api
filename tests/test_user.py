def test_empty_db(client):
    response = client.get('/user')
    assert b'[]' in response.data


def test_create_user(client):
    response = client.post(
        '/user', json={'name': 'Jane Doe', 'email': 'jane@example.com', 'age': 27})
    assert response.status_code == 200


def test_duplicate_user(client):
    client.post(
        '/user', json={'name': 'Jane Doe', 'email': 'jane@example.com', 'age': 27})
    response = client.post(
        '/user', json={'name': 'Jane Doe', 'email': 'jane@example.com', 'age': 27})
    assert response.status_code == 409


def test_no_name(client):
    response = client.post(
        '/user', json={'email': 'jane@example.com', 'age': 27})
    assert response.status_code == 400


def test_empty_name(client):
    response = client.post(
        '/user', json={'name': '', 'email': 'jane@example.com', 'age': 27})
    assert response.status_code == 400


def test_no_email(client):
    response = client.post(
        '/user', json={'name': 'Jane Doe', 'age': 27})
    assert response.status_code == 400


def test_invalid_email(client):
    response = client.post(
        '/user', json={'name': 'Jane Doe', 'email': 'thisisnotanemail', 'age': 27})
    assert response.status_code == 400
