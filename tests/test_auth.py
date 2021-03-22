import pytest
from flask import g,session
from flaskr.db import get_db


# 测试注册视图
def test_register(client,app):
    assert client.get('auth/register').status_code ==200
    response = client.post(
        '/auth/register',data={'username':'a','password':'a'}
    )
    # 数据合法时是否重定向到login页面，当注册视图重定向到登录视图时， headers 会有一个包含登录 URL 的 Location 头部。
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "select * from user where username = 'a'"
        ).fetchone() is not None


    @pytest.mark.parametrize(('username','password','message'),(
        ('','',b'Username isrequired.'),
        ('a', '', b'Password is required.'),
        ('test', 'test', b'already registered'),
    ))
    def test_register_validate_input(client,username,password,message):
        response = client.post(
            '/auth/register',
            data={'username':username,'password':password}
        )
        assert message in response.data


# 测试登录视图
def test_login(client,auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login
    assert 'http://localhost' == response.headers['Location']

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data