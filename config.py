import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECCRET_KEY') or 'Sucherly'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Flask-SQLAlchemy 追踪对象的修改并且发送信号功能关闭

    # 邮件配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    FLASKY_MAIL_SENDER = 'Flasky Sucherly <example@qq.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_MAIL_SUBJECT_PREFIX = os.environ.get('FLASKY_MAIL_SUBJECT_PREFIX') or "[SUCH_TEST_WEB]"
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # 上传文件配置
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    DOWNLOAD_FOLDER = os.environ.get('DOWNLOAD_FOLDER')

    # 接口测试配置
    is_log = False  # 是否开启日志
    api_timeout = 60
    http_log_info = "case_http_info.log"  # http输出信息日志
    is_headers = False  # http_info*.log中是否记录request.header
    is_body = False  # http_info*.log中是否记录request.body
    is_response = False  # http_info*.log中是否记录response
    is_stack = False
    http_log_conn = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,
                                                                                                'data-dev.sqlite') + '?check_same_thread=False'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,
                                                                                                 'data-test.sqlite') + '?check_same_thread=False'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "sqlite:///" + os.path.join(basedir,
                                                                                            "data.sqlite") + "?check_same_thread=False"

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        # 出错时邮件通知管理员
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, "MAIL_USERNAME", None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' 应用程序错误',
            credentials=credentials,
            secure=secure,
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}
