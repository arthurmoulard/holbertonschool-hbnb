#!/usr/bin/python3
from app.models.BaseModel import BaseModel


class Review(BaseModel):

    def __init__(self, text, rating, place, user):
        if not text or not isinstance(text, str):
            raise ValueError("The content of the review is mandatory")

        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("The rating must be an integer between 1 and 5")

        if place is None:
            raise ValueError("The review must be linked to a valid Place")
        if user is None:
            raise ValueError("The review must have a valid author(User)")

        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
