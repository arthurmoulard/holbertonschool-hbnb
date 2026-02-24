#!/usr/bin/python3
import uuid
from datetime import datetime
import BaseModel


class Place(BaseModel):
    def __init__(self, id, title, description, price, latitude, longitude, owner):
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

    @property
    def title(self):
        return self.title
    
    @title.setter
    def title(self, char):
        if not char or isinstance(char, str):
            raise TypeError("Le titre est obligatoire et doit etre une chaine de caractères.")
        if len(char) > 100:
            raise ValueError("Le titre ne peut pas dépasser 100 caractères.")
    
    @property
    def price(self):
        return self.price
    
    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Le prix doit être un nombre positif.")
        self._price = float(value)
    
    @property
    def longitude(self):
        return self.longitude
    
    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or not (-180.0 <= value <= 180.0):
            raise ValueError("La longitude doit être comprise entre -180.0 et 180.0.")
        self._longitude = float(value)
    
    @property
    def latitude(self):
        return self.latitude
    
    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float))or not (-90.0 <= value <= 90.0):
            raise ValueError("La latitude doit être comprise entre -90.0 et 90.0.")
        self._latitude = float(value)
    
    @property
    def owner(self):
        return self.owner
    
    @owner.setter
    def owner(self, user):
        if not user or not hasattr(user, 'id'):
            raise ValueError("Le propriétaire doit être une instance valide de User.")
        self._owner = user


    def add_review(self, review):
        if not hasattr(review, 'id'):
            raise ValueError("L'avis doit être une instance valide de Review.")
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity):
        if not hasattr(amenity, 'id'):
            raise ValueError("L'équipement doit être une instance valide de Amenity.")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()

    def save(self):
        self.update_at = datetime.now()

    def repr(self):
        return f"<Place id={self.id} title='{self.title} owner={self.owner.id}>"