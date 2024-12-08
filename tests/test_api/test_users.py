STATUS_OK = 200
STATUS_CREATED = 201
STATUS_NO_CONTENT = 204
STATUS_BAD_REQUEST = 400
access_token = None


async def test_user_registration(client):
    """ Test user registration """
    response = await client.post(
        '/auth/register',
        json={
            'username': 'test1',
            'password': 'test1234',
        },
    )
    assert response.status_code == STATUS_CREATED
    assert response.json()['username'] == 'test1'
    assert response.json()['role'] == 'client'


async def test_user_login(client, get_test_session):
    """ Test user login with returning JWT access token """
    global access_token
    response = await client.post(
        '/auth/jwt/login',
        data={
            'username': 'test1',
            'password': 'test1234',
        },
    )
    assert response.status_code == STATUS_OK
    assert response.json()['token_type'] == 'bearer'
    assert 'access_token' in response.json()
    access_token = response.json().get('access_token')


async def test_user_logout(client, get_test_session):
    """ Test user logout with JWT access token in headers """
    response = await client.post(
        '/auth/jwt/logout',
        headers={
            'Authorization': f'Bearer {access_token}',
        },
    )
    assert response.status_code == STATUS_NO_CONTENT
