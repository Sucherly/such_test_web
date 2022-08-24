import os

from flask import Flask
from flask_apscheduler import APScheduler
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy



from config import config

db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()
scheduler = APScheduler()
# login_view设置登录页面的端点，auth.login是登录蓝本的名称。
login_manager.login_view = 'user_api.login'

def create_app(config_name):
    app = Flask(__name__)
    # print(os.path.abspath('frontend/build'))
    # app = Flask(__name__, static_folder='app/frontend/build',static_url_path='/')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"  # 指定浏览器渲染的文件类型，和解码格式
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

    # login_manager.init_app(app)

    # 配置api权限验证的回调函数
    @scheduler.authenticate
    def authenticate(auth):
        return auth['username'] == 'guest' and auth['password'] == 'guest'

    # 注册api蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # 注册api_user蓝本
    from .api.users import user_api as user_v1_blueprint
    app.register_blueprint(user_v1_blueprint, url_prefix='/api')

    # 注册api蓝本
    from .api import api as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix='/api')



    return app

