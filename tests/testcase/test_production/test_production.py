import unittest

from app.models import Production
from tests.models import my_test_case
from tests.page.production_page import ProductionPage


class Productions(my_test_case.MyTestCase):
    """产品版块测试"""

    def test_get_productions(self):
        """获取所有产品"""
        page = ProductionPage()
        response = self.client.post('/api/productions',headers=page.get_api_headers(self.default_email,self.default_password))
        self.assertEqual(response.status_code, 200)
        res = Production.query.all()
        data = [dt.to_json() for dt in res]
        self.assertEqual(response.json, page.option_ok(data))


if __name__ == '__main__':
    unittest.main()