from app.models.BaseModel import BaseModel
from email_validator import validate_email, EmailNotValidError
from flask_bcrypt import generate_password_hash, check_password_hash


class User(BaseModel):
    """Model representing a user in the system."""

    def __init__(self, first_name, last_name, email, password):
        """Initialize a new User instance with validation."""
        super().__init__()
        self.__first_name = None
        self.first_name = first_name
        self.__last_name = None
        self.last_name = last_name
        self.__email = None
        self.email = email
        self.is_admin = False
        self.reviews = []
        self.places = []
        self.__password = None
        self.hash_password(password)  # passe par hash_password au lieu du setter

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        if not value:
            raise ValueError("first_name cannot be empty")
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if not value:
            raise ValueError("last name cannot be empty")
        self.__last_name = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not value:
            raise ValueError("email cannot be empty")
        try:
            valid = validate_email(value, check_deliverability=False)
            self.__email = valid.normalized
        except EmailNotValidError:
            raise ValueError("Invalid email address format")

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value

    def hash_password(self, password):
        """Hashes the password before storing it."""
        if not password:
            raise ValueError("password cannot be empty")
        self.__password = generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return check_password_hash(self.__password, password)

    def add_review(self, review):
        self.reviews.append(review)

    def add_place(self, place):
        self.places.append(place)