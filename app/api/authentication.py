from functools import wraps

from flask import g, jsonify, Response, make_response
from flask_httpauth import HTTPBasicAuth

from app.api import api
from app.api.check_info import option_ok
from app.api.errors import unauthorized, forbidden
from app.models import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    """验证密码"""
    if email_or_token == '':
        return False
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_user = True
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_user = False
    return user.verify_password(password)

@auth.error_handler
def auth_error():
    return unauthorized('非法认证')

@api.before_request
@auth.login_required
def before_request():
    # if not g.current_user.is_anonymous and \
    #         not g.current_user.true_name:
    #     return forbidden('未确认用户，真实姓名需维护')
    return None

@api.route('/get_token', methods=['POST'])
def get_auth_token():
    """获取令牌"""
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('非法认证')
    return option_ok({'token': g.current_user.generate_auth_token(expiration=3600), 'expiration': 3600})

