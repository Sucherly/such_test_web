from app.models import User
from tests.page.base import Base


class UserPage(Base):
    def __init__(self):
        super().__init__()

    def to_json(self,email):
        user=User.query.filter_by(email=email).first()
        data={
            'username': user.name,
            'true_name': user.true_name,
            'member_since': self.time_to_gmt(user.member_since),
            'last_seen': self.time_to_gmt(user.last_seen),
        }
        return data
