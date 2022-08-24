from flask import request, url_for
from flask_login import login_user, login_required, logout_user

from app import db
from app.api.check_info import duplicated, field_superfluous, option_ok, option_null, not_fund
from app.api.users import user_api
from app.models import User


@user_api.route('/register', methods=['POST'])
def register():
    """注册用户"""
    res=request
    user_data = request.json
    # 判断用户是否存在
    user = User.query.filter_by(email=user_data['email']).first()
    if user:
        del user_data['password']
        response = duplicated(user_data, '用户已存在，无需注册！')
    else:
        user = User(email=user_data['email'], name=user_data['name'], password=user_data['password'])
        superfluous = [k for k in user_data.keys() if
                       not hasattr(user, k) and k not in ['password', 'password2', 'remember_me']]
        db.session.add(user)
        db.session.commit()
        # 再次查询数据库
        user = User.query.filter_by(email=user_data['email']).first()
        if not user:
            del user_data['password']
            response = option_null(user_data)
        elif superfluous:
            response = field_superfluous(user.to_json(), '用户已注册！但请求数据存在多余的字段：值',
                                         field_superfluous=superfluous)
        else:
            response = option_ok(user.to_json())
    if 'remember_me' in user_data and user_data['remember_me'] == 'on':
        login_user(user, True)
    return response


@user_api.route('/login', methods=['POST'])
def login():
    """登录用户"""
    user_data = request.json
    # 判断用户是否存在
    user = User.query.filter_by(email=user_data['email']).first()
    if user is not None and user.verify_password(user_data['password']):
        remember_me = True if 'remember_me' in user_data and user_data['remember_me'] else False
        login_user(user, remember_me)
        return option_ok(user.to_json(), **{'token': user.generate_auth_token(expiration=3600), 'expiration': 3600})
    response = not_fund(user_data['email'])
    return response


@user_api.route('/user_true_name', methods=['POST'])
def user_true_name():
    """设置真实姓名"""
    # 更新数据
    user_data = request.json
    user = User.query.filter_by(email=user_data['email']).first_or_404()
    user.true_name = user_data['true_name']
    db.session.add(user)
    db.session.commit()
    # 再次查询数据返回
    user_query = User.query.filter_by(email=user_data['email']).first_or_404()
    if user_query.true_name != user_data['true_name']:
        return option_null(user_query.to_json())
    return option_ok(user_query.to_json())


@user_api.route('/get_true_name', methods=['GET'])
def get_user_true_name():
    user = User.query.filter_by(email='admin@qq.com').first()
    print(user.true_name)
    return user.true_name


@user_api.route('/info_test', methods=['GET'])
def get_info():
    return {'msg': '测试返回信息'}


@user_api.route('/logout')
@login_required
def logout():
    logout_user()
    return option_ok('退出登录成功！')
