from app.models.users import User
from app.models.places import Place
from app.models.amenities import Amenity
from app.models.reviews import Review
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ── Users ─────────────────────────────────────────────────────────────

    def create_user(self, user_data):
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data['password'],
            is_admin=user_data.get('is_admin', False)
        )
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_user(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data, is_admin=False):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(user_data, is_admin=is_admin)
        return user

    # ── Amenities ─────────────────────────────────────────────────────────

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        return amenity

    # ── Places ────────────────────────────────────────────────────────────

    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        user = self.user_repo.get(owner_id)
        if not user:
            raise ValueError("Owner not found")

        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=user
        )
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
        place.update(place_data)
        return place

    def delete_place(self, place_id):
        if not self.place_repo.delete(place_id):
            raise ValueError("Place not found")

    # ── Reviews ───────────────────────────────────────────────────────────

    def create_review(self, review_data):
        user = self.user_repo.get(review_data.get('user_id'))
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(review_data.get('place_id'))
        if not place:
            raise ValueError("Place not found")

        if not isinstance(review_data.get('rating'), int) or \
                not (1 <= review_data['rating'] <= 5):
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
        return [r for r in self.review_repo.get_all()
                if r.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        if 'rating' in review_data:
            if not isinstance(review_data['rating'], int) or \
                    not (1 <= review_data['rating'] <= 5):
                raise ValueError("Rating must be between 1 and 5")
        review.update(review_data)
        return review

    def delete_review(self, review_id):
        if not self.review_repo.delete(review_id):
            raise ValueError("Review not found")
        