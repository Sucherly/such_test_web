# 自定义过滤器：根据id获取case_name
from app.models import Production
from such_test_web import app


@app.template_filter("product_name")
def product_name(product):
    if id:
        res = Production.query.filter_by(id=product).first()
        return res.name if res else ''
