import os
from flask_migrate import Migrate, upgrade, init

from app import create_app, db
from app.models import Production, ProField, User, ProInterface, CommonField

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    """上下文设置"""
    return dict(db=db, User=User, Production=Production, ProField=ProField, ProInterface=ProInterface,CommonField=CommonField)


@app.cli.command()
def create():
    """初次安装时运行"""
    # 创建数据库以及创建表
    db.create_all()
    # 数据库表设置初始数据
    Production.create_default_productions()
    CommonField.create_default_field()
    # migrate初始化，创建migrations
    init()


@app.cli.command()
def deploy():
    """安装升级时运行"""
    upgrade()
    Production.create_default_productions()
    CommonField.create_default_field()

@app.template_filter("product_name")
def product_name(product):
    if id:
        res = Production.query.filter_by(id=product).first()
        return res.name if res else ''

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') or False, host='0.0.0.0', port='8000')
