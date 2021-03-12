import os
from flask import Flask

def create_app(test_config=None):
    # 建立并配置应用程序
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path,'flaskr.sqlite'),
    )

    if test_config is None:
        # 不测试时加载实例配置（如果存在）
        app.config.from_pyfile('config.py',silent=True)
    else:
        # 如果test_config传入值则加载测试配置
        app.config.from_mapping(test_congfig)

    # 确保实例文件夹存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 一个简单的页面
    @app.route('/hello')
    def hello():
        return 'Hello,World!'


    from . import db
    db.init_app(app)


    from . import auth
    app.register_blueprint(auth.bp)

    return app