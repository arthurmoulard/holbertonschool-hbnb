from app import db
from app.models.BaseModel import BaseModel
from sqlalchemy.orm import validates

# Table d'association many-to-many Place <-> Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36),
              db.ForeignKey('places.id', ondelete='CASCADE'),
              primary_key=True),
    db.Column('amenity_id', db.String(36),
              db.ForeignKey('amenities.id', ondelete='CASCADE'),
              primary_key=True)
)


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # Clé étrangère vers User
    owner_id = db.Column(
        db.String(36),
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    # Relations
    owner = db.relationship(
        'User',
        backref=db.backref('places', lazy=True, cascade='all, delete-orphan')
    )
    amenities = db.relationship(
        'Amenity',
        secondary=place_amenity,
        lazy='subquery',
        backref=db.backref('places', lazy=True)
    )

    @validates('title')
    def validate_title(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("title is required and must be a string")
        if len(value) > 100:
            raise ValueError("title cannot exceed 100 characters")
        return value

    @validates('price')
    def validate_price(self, key, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("price must be a positive number")
        return float(value)

    @validates('latitude')
    def validate_latitude(self, key, value):
        if value is not None:
            if not isinstance(value, (int, float)) or \
                    not (-90.0 <= value <= 90.0):
                raise ValueError(
                    "latitude must be between -90.0 and 90.0")
        return value

    @validates('longitude')
    def validate_longitude(self, key, value):
        if value is not None:
            if not isinstance(value, (int, float)) or \
                    not (-180.0 <= value <= 180.0):
                raise ValueError(
                    "longitude must be between -180.0 and 180.0")
        return value

    def to_dict(self):
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