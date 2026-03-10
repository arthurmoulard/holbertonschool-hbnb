from app.persistence.repository import InMemoryRepository
from app.models.users import User
from app.models.places import Place
from app.models.amenities import Amenity
from app.models.reviews import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

# --------------------- User ---------------------

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_user(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            return None
        self.user_repo.update(user_id, user_data)
        return self.get_user(user_id)

# --------------------- Amenity ---------------------

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None

        for key, value in amenity_data.items():
            setattr(amenity, key, value)
        return amenity

# --------------------- Place ---------------------

    def create_place(self, place_data):
        price = place_data.get("price", 0)
        if price < 0:
            raise ValueError("Price must be positive")

        latitude = place_data.get("latitude")
        if latitude is not None and not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")

        longitude = place_data.get("longitude")
        if longitude is not None and not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")

        owner_id = place_data.pop("owner_id")
        user = self.user_repo.get(owner_id)

        if not user:
            raise ValueError("Owner not found")

        place = Place(owner=user, **place_data)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        # On met à jour seulement les champs envoyés
        if 'title' in place_data:
            place.title = place_data['title']
        if 'description' in place_data:
            place.description = place_data['description']
        if 'price' in place_data:
            place.price = place_data['price']
        if 'latitude' in place_data:
            place.latitude = place_data['latitude']
        if 'longitude' in place_data:
            place.longitude = place_data['longitude']

        return place

# --------------------- Review ---------------------

    def create_review(self, review_data):
        user = self.user_repo.get(review_data.get('user_id'))
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(review_data.get('place_id'))
        if not place:
            raise ValueError("Place not found")

        rating = review_data.get('rating')
        if rating is None or not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return \
            [r for r in self.review_repo.get_all() if r.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")

        if 'rating' in review_data:
            rating = review_data['rating']
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5")

        self.review_repo.update(review_id, review_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        self.review_repo.delete(review_id)
