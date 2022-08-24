import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECCRET_KEY') or 'Sucherly'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Flask-SQLAlchemy 追踪对象的修改并且发送信号功能关闭

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
    MAIL_USERNAME="ling.kaito@qq.com"
    MAIL_PASSWORD=" smtp.qq.com"
    MAIL_SERVER="smtp.qq.com"
    MAIL_PORT="465" # qq是465或587
    FLASKY_ADMIN="ling.kaito@qq.com"
    FLASKY_MAIL_SUBJECT_PREFIX='SUCH_TEST_WEB'

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
            fromaddr=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' 应用程序错误',
            credentials=credentials,
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}