from app.models.BaseModel import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        # Validation avant tout
        if not text or not isinstance(text, str):
            raise ValueError("text is required and must be a string")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("rating must be an integer between 1 and 5")
        if place is None or not hasattr(place, 'id'):
            raise ValueError("review must be linked to a valid Place")
        if user is None or not hasattr(user, 'id'):
            raise ValueError("review must have a valid author (User)")

        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user.id,
            'place_id': self.place.id
        }