from app.api import api
from app.api.check_info import option_ok
from app.models import User


@api.route('/user/<email>', methods=['GET'])
def get_user(email):
    """查询用户"""
    user = User.query.filter_by(email=email).first_or_404()
    return option_ok(user.to_json())
