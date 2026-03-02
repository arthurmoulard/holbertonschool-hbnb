#!/usr/bin/python3
from app.models.BaseModel import BaseModel
from flask_restx import Namespace, fields


api = Namespace('places', description='Place operations')

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
})

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float
    (required=True, description='Latitude of the place'),
    'longitude': fields.Float
    (required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List
    (fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List
    (fields.Nested(review_model), description='List of reviews')
})


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, char):
        if not char or not isinstance(char, str):
            raise TypeError
        ("Le titre est obligatoire et doit etre une chaine de caractères.")
        if len(char) > 100:
            raise ValueError("Le titre ne peut pas dépasser 100 caractères.")
        self._title = char

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Le prix doit être un nombre positif.")
        self._price = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or not\
                (-180.0 <= value <= 180.0):
            raise ValueError
        ("La longitude doit être comprise entre -180.0 et 180.0.")
        self._longitude = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or not (-90.0 <= value <= 90.0):
            raise ValueError
        ("La latitude doit être comprise entre -90.0 et 90.0.")
        self._latitude = float(value)

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, user):
        if not user or not hasattr(user, 'id'):
            raise ValueError
        ("Le propriétaire doit être une instance valide de User.")
        self._owner = user

    @property
    def owner_id(self):
        return self._owner.id

    def add_review(self, review):
        if not hasattr(review, 'id'):
            raise ValueError("L'avis doit être une instance valide de Review.")
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity):
        if not hasattr(amenity, 'id'):
            raise ValueError
        ("L'équipement doit être une instance valide de Amenity.")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()

    def __repr__(self):
        return f"<Place id={self.id}\
                title='{self.title} owner={self.owner.id}>"
