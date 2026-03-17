from app.models.BaseModel import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price,
                 latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    # ── Propriétés ───────────────────────────────────────────────────────────

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("title is required and must be a string")
        if len(value) > 100:
            raise ValueError("title cannot exceed 100 characters")
        self._title = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("price must be a positive number")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or \
                not (-90.0 <= value <= 90.0):
            raise ValueError("latitude must be between -90.0 and 90.0")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or \
                not (-180.0 <= value <= 180.0):
            raise ValueError("longitude must be between -180.0 and 180.0")
        self._longitude = float(value)

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, user):
        if not user or not hasattr(user, 'id'):
            raise ValueError("owner must be a valid User instance")
        self._owner = user

    @property
    def owner_id(self):
        return self._owner.id

    # ── Méthodes ─────────────────────────────────────────────────────────────

    def add_review(self, review):
        if not hasattr(review, 'id'):
            raise ValueError("review must be a valid Review instance")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        if not hasattr(amenity, 'id'):
            raise ValueError("amenity must be a valid Amenity instance")
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def to_dict(self):
        """Version légère pour les listes."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id
        }

    def to_dict_detailed(self):
        """Version complète avec owner et amenities pour GET /<place_id>."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': self.owner.to_dict(),
            'amenities': [
                {'id': a.id, 'name': a.name} for a in self.amenities
            ]
        }