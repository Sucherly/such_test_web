from app.models import Production
from tests.page.base import Base


class ProductionPage(Base):
    def __init__(self):
        super().__init__()

    def to_json(self, email):
        res = Production.query.filter_by(email=email).first()
        """转换json"""
        json = {
            'id': res.id,
            'name': res.name,
            'description': res.description,
        }
        return json
