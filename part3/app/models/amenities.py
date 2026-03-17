from app.models.BaseModel import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        if not name:
            raise ValueError("name cannot be empty")
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if len(name) > 50:
            raise ValueError("name must be at most 50 characters")

        super().__init__()
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
    