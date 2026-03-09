#!/usr/bin/python3
from app.models.BaseModel import BaseModel


class Amenity(BaseModel):
    """id (String): Unique identifier for each amenity.
    name (String): The name of the amenity (e.g., "Wi-Fi", "Parking").
    Required, maximum length of 50 characters.
    created_at (DateTime): Timestamp when the amenity is created.
    updated_at (DateTime): Timestamp when the amenity is last updated"""

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.places = []

        if not name:
            raise ValueError("name can't be empty")

        if not isinstance(name, str):
            raise TypeError("name must be a string")

        if len(name) > 50:
            raise ValueError("name must be at most 50 characters")

    def add_place(self, place):
        self.places.append(place)
