from app import db
from app.models.BaseModel import BaseModel
from sqlalchemy.orm import validates


class Review(BaseModel):
    __tablename__ = 'reviews'
    __table_args__ = (
        # Un user ne peut reviewer qu'une seule fois par place
        db.UniqueConstraint(
            'user_id', 'place_id', name='unique_user_place_review'
        ),
    )

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Clés étrangères
    user_id = db.Column(
        db.String(36),
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    place_id = db.Column(
        db.String(36),
        db.ForeignKey('places.id', ondelete='CASCADE'),
        nullable=False
    )

    # Relations
    user = db.relationship(
        'User',
        backref=db.backref('reviews', lazy=True, cascade='all, delete-orphan')
    )
    place = db.relationship(
        'Place',
        backref=db.backref('reviews', lazy=True, cascade='all, delete-orphan')
    )

    @validates('rating')
    def validate_rating(self, key, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("rating must be an integer between 1 and 5")
        return value

    @validates('text')
    def validate_text(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("text is required and must be a string")
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id
        }