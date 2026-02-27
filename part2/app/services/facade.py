from app.persistence.repository import InMemoryRepository
from app.models.users import User
from app.models.amenities import Amenity
from app.models.reviews import Review
# from app.models.amenities import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

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
        for key, value in user_data.items():
            setattr(user, key, value)
        return user

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        return self.place_repo.get(place_id)

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

    def create_review(self, review_data):
        text = review_data.get("text")
        rating = review_data.get("rating")
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")

        if not text or not user_id or not place_id:
            raise ValueError("Missing required fields")

        if rating is None or rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        user = self.get_user(user_id)
        place = self.get_place(place_id)

        if not user:
            raise ValueError("User not found")

        if not place:
            raise ValueError("Place not found")

        review = Review(text, rating, user_id, place_id)

        self.storage.save(review)
        place.reviews.append(review)

        return review

    def get_review(self, review_id):
        return self.storage.get(Review, review_id)

    def get_all_reviews(self):
        return self.storage.all(Review)

    def get_reviews_by_place(self, place_id):
        return [r for r in self.review_repo.get_all()
                if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None

        if "text" in review_data:
            review.text = review_data["text"]

        if "rating" in review_data:
            rating = review_data["rating"]
            if rating < 1 or rating > 5:
                raise ValueError("Rating must be between 1 and 5")
            review.rating = rating

        self.storage.save(review)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return None

        place = self.get_place(review.place_id)
        if place and review in place.reviews:
            place.reviews.remove(review)

        self.storage.delete(review)
        return True
