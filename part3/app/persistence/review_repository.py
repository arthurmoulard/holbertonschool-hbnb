from app.persistence.repository import SQLAlchemyRepository
from app.models.reviews import Review


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    def get_by_place(self, place_id):
        return self.model.query.filter_by(place_id=place_id).all()

    def get_by_user(self, user_id):
        return self.model.query.filter_by(user_id=user_id).all()