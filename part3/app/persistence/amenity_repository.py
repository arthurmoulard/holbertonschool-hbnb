from app.persistence.repository import SQLAlchemyRepository
from app.models.amenities import Amenity


class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)

    def get_by_name(self, name):
        return self.model.query.filter_by(name=name).first()