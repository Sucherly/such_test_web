import unittest
from tests.models import my_test_case
from tests.page.user_page import UserPage


class UserLogin(my_test_case.MyTestCase):
    """用户登录测试"""

    def test_login(self):
        """登录用户"""
        page = UserPage()
        data = {"email": self.default_email, "password": self.default_password,"remember_me":"on"}
        response = self.client.post('/api/login', json=data)
        self.assertEqual(response.status_code, 200)
        print(response.json)
        self.assertEqual(response.json, page.option_ok(page.to_json(data['email']),**{'token': page.get_token(data['email'],data['password']), 'expiration': 3600}))


if __name__ == '__main__':
    unittest.main()
