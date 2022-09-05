from datetime import datetime

from tests.models import my_test_case
from tests.page.user_page import UserPage


class UserRegister(my_test_case.MyTestCase):
    """用户版块测试"""

    def test_register(self):
        """注册用户"""
        page = UserPage()
        name = 'test' + datetime.now().strftime("%Y-%m-%d")
        data = {"email": "{}@qq.com".format(name), "name": name, "password": "test" + name}
        response = self.client.post('/api/register', json=data)
        self.assertEqual(response.status_code, 200)
        print(response.json)
        self.assertEqual(response.json, page.option_ok(page.to_json(data['email'])))