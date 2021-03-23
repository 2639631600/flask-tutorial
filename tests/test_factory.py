from flaskr import create_app


# 测试工厂
def test_config():
    assert not create_app().testing  # 断言create_app没有设置调试模式
    assert create_app({'TESTING': True}).testing  # 添加调试模式


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello,World!'
