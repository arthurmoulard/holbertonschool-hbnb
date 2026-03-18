from app.persistence.repository import SQLAlchemyRepository
from app.models.users import User


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email):
        return self.model.query.filter_by(email=email).first()