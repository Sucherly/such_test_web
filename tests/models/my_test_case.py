import os
import shutil
import unittest

from flask_migrate import init

from app import create_app, db
from app.models import Production, CommonField, User
from tests.utils.my_file import get_migration_dir


# 当前环境数据库是否已有迁移，如果已有迁移，那么本次测试均不生成迁移，也不会清理迁移目录


class MyTestCase(unittest.TestCase):
    """自定义测试基类"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.migration_dir = get_migration_dir()
        self.is_migration = os.path.exists(get_migration_dir())
        self.default_email = "test@qq.com"
        self.default_password = "test@qq.com"
        self.default_name = "test测试默认账号"

    def setUp(self) -> None:
        # 创建测试环境app
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        # 创建数据库以及创建表
        db.create_all()
        # 数据库表设置初始数据
        Production.create_default_productions()
        CommonField.create_default_field()
        # migrate初始化，创建migrations
        if not self.is_migration:
            init()
            self.is_migration = False
        # 创建客户端
        self.client = self.app.test_client()
        # 向数据库中插入一条默认测试用户
        self.default_user = User(email=self.default_email, password=self.default_password, name=self.default_name)
        db.session.add(self.default_user)
        db.session.commit()

    def tearDown(self):
        # 清理迁移目录
        if not self.is_migration:
            shutil.rmtree(self.migration_dir)
        # 清理数据库并删除
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
