from datetime import datetime

from authlib.jose import jwt, JoseError
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy import UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


# 产品接口版块
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String(64), unique=True, nullable=False)  # 用户邮箱
    password_hash = db.Column(db.String(128), nullable=False)  # 密码
    name = db.Column(db.Text, unique=True, nullable=False)  # 用户名
    telephone = db.Column(db.String(64))  # 手机号
    true_name = db.Column(db.Text)  # 真实姓名
    address = db.Column(db.Text)  # 联系地址
    post = db.Column(db.String(64))  # 岗位
    department = db.Column(db.String(64))  # 部门
    about_me = db.Column(db.Text())  # 用户介绍
    member_since = db.Column(db.DateTime(), default=datetime.utcnow())  # 注册日期
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow())  # 最后访问日期

    def __repr__(self):
        return '<User %r>' % self.name

    @property
    def password(self):
        """限制密码不可读取"""
        raise AttributeError('密码不可读')

    @password.setter
    def password(self, pwd):
        """设置密码"""
        self.password_hash = generate_password_hash(pwd)

    def verify_password(self, pwd):
        """校验密码"""
        res = check_password_hash(self.password_hash, pwd)
        return check_password_hash(self.password_hash, pwd)

    def ping(self):
        """刷新用户的最后访问时间"""
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def generate_auth_token(self, expiration, **kwargs):
        """使用用户id编码后生成令牌"""

        # 签名算法
        header = {'alg': 'HS256'}
        # 用于签名的密钥
        key = current_app.config['SECRET_KEY']
        # 待签名的数据负载
        data = {'id': self.id}
        if kwargs: data.update(**kwargs)
        return jwt.encode(header=header, payload=data, key=key).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        """令牌验证后返回用户id"""
        key = current_app.config['SECRET_KEY']
        try:
            data = jwt.decode(token, key)
            print(data)
        except JoseError:
            return False
        return User.query.get(data['id'])

    def to_json(self):
        """转换json"""
        json_user = {
            'username': self.name,
            'true_name': self.true_name,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
        }
        return json_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


# 产品接口版块
class Production(db.Model):
    """产品模型"""
    __tablename__ = 'productions'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.Text, unique=True, nullable=False)  # 产品名称
    description = db.Column(db.Text, nullable=False)  # 产品简介

    pro_field = db.relationship('ProField', backref='production', lazy='dynamic')
    pro_interface = db.relationship('ProInterface', backref='production', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.name

    @staticmethod
    def create_default_productions():
        """创建默认存在的产品数据--本平台"""
        data = [
            {'name': 'such_test_web', 'description': '本平台'},
        ]
        for dt in data:
            production = Production.query.filter_by(name=dt['name']).first()
            if not production:
                production = Production()
            for k, v in dt.items():
                if hasattr(Production, k):
                    setattr(production, k, v)
            db.session.add(production)
        db.session.commit()

    def to_json(self):
        """转换json"""
        json = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }
        return json


class CommonField(db.Model):
    """公共字段表模型"""
    __tablename__ = 'common_fields'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.Text, nullable=False)  # 字段名称
    description = db.Column(db.Text, nullable=False)  # 字段简介
    data_type = db.Column(db.String(64), nullable=False)  # 数据类型
    eg = db.Column(db.Text, nullable=False)  # 示例

    def __repr__(self):
        return '<User %r>' % self.name

    @staticmethod
    def create_default_field():
        """初始化数据
        注意在此之前需先调用create_default_productions()进行Productions表的数据初始化
        """
        production = Production.query.filter_by(name='such_test_web').first()
        if not production:
            raise ValueError('未创建产品，请先执行create_default_productions()')
        data = [
            {'name': 'int', 'description': '整数(整型，长整型等)', 'data_type': 'integer,long', 'eg': '1'},
            {'name': 'float', 'description': '浮点数', 'data_type': 'single,double,REAL', 'eg': '1.1'},
            {'name': 'string', 'description': '字符串,指定长度', 'data_type': 'char,string', 'eg': 'this'},
            {'name': 'text', 'description': '可变长度', 'data_type': 'varchar,text', 'eg': 'change length'},
        ]
        for dt in data:
            field = CommonField.query.filter_by(name=dt['name']).first()
            if not field:
                field = CommonField()
            for k, v in dt.items():
                if hasattr(CommonField, k):
                    setattr(field, k, v)
            db.session.add(field)
        db.session.commit()


class ProField(db.Model):
    """字段表模型"""
    __tablename__ = 'pro_fields'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.Text, nullable=False)  # 字段名称
    description = db.Column(db.Text, nullable=False)  # 字段简介
    product = db.Column(db.Integer, db.ForeignKey('productions.id'), nullable=False)  # 产品表(productions)的外键，关联于id
    data_type = db.Column(db.String(64), nullable=False)  # 数据类型
    eg = db.Column(db.Text, nullable=False)  # 示例

    def __repr__(self):
        return '<User %r>' % self.name


class ProInterface(db.Model):
    """接口模型"""
    __tablename__ = 'pro_interfaces'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.Text, nullable=False)  # 接口名称
    url = db.Column(db.Text, nullable=False)  # 接口路由
    description = db.Column(db.Text, nullable=False)  # 接口简介
    version = db.Column(db.Integer, nullable=False)  # 接口版本
    product = db.Column(db.Integer, db.ForeignKey('productions.id'), nullable=False)  # 产品表(productions)的外键，关联于id
    request_params = db.Column(db.Text)  # 接口入参。字段名:字段类型。多个字段以英文逗号分隔
    response_params = db.Column(db.Text)  # 接口出参。字段名:字段类型。多个字段以英文逗号分隔
    status = db.Column(db.Integer, nullable=False, default=0)  # 状态。0--启用，1--已弃用，2--未完全弃用，已有新接口代替，逐步弃用中
    module = db.Column(db.String(64), nullable=False)  # 功能版块
    request_type = db.Column(db.String(64), nullable=False)  # 请求方式
    UniqueConstraint('name', 'version', name='uq_name_version')  # name,version联合唯一

    def __repr__(self):
        return '<User %r>' % self.name

    def to_json(self):
        """转换json"""
        json = {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'description': self.description,
            'version': self.version,
            'product': self.product,
            'request_params': self.request_params,
            'response_params': self.response_params,
            'status': self.status,
            'module': self.module,
            'request_type': self.request_type
        }
        return json

    def status_corresponding(self):
        """状态的中文"""
        desc = ['启用', '已弃用', '未完全弃用，已有新接口代替']
        return desc[self.status]
