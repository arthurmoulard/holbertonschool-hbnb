from app.models.BaseModel import BaseModel
from email_validator import validate_email, EmailNotValidError
import bcrypt
import re


class User(BaseModel):
    """Model representing a user in the system.

    Inherits from BaseModel and adds attributes for the user's name,
    email, admin status, and associated reviews and places.

    Attributes:
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (str): Email address of the user.
        is_admin (bool): Whether the user has admin privileges.
        reviews (list): List of Review objects created by the user.
        places (list): List of Place objects owned by the user.
    """

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
        self.password = password

    @property
    def first_name(self):
        """str: Get the user's first name."""
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        """Set the user's first name.

        Args:
            value (str): First name.

        Raises:
            ValueError: If the first name is empty or None.
        """
        if not value:
            raise ValueError("first_name cannot be empty")
        if len(value) > 50:
            raise ValueError("First name must be at most 50 characters")
        self.__first_name = value

    @property
    def last_name(self):
        """str: Get the user's last name."""
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        """Set the user's last name.

        Args:
            value (str): Last name.

        Raises:
            ValueError: If the last name is empty or None.
        """
        if not value:
            raise ValueError("last name cannot be empty")
        if len(value) > 50:
            raise ValueError("Last name must be at most 50 characters")
        self.__last_name = value

    @property
    def email(self):
        """str: Get the user's email address."""
        return self.__email

    @email.setter
    def email(self, value):
        """Set the user's email address with validation.

        Args:
            value (str): Email address.

        Raises:
            ValueError: If the email is empty or has invalid format.
        """
        if not value:
            raise ValueError("email cannot be empty")

        try:
            valid = validate_email(value, check_deliverability=False)
            self.__email = valid.normalized
        except EmailNotValidError:
            raise ValueError("Invalid email address format")

    def add_review(self, review):
        """Add a review to the user.

        Args:
            review: A Review object to associate with this user.
        """
        self.reviews.append(review)

    def add_place(self, place):
        """Add a place to the user.

        Args:
            place: A Place object to associate with this user.
        """
        self.places.append(place)

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if not value:
            raise ValueError("Password cannot be empty")
        if len(value) < 8:
            raise ValueError("password must be at least 8 characters")
        if len(value) > 50:
            raise ValueError("password must be at most 50 characters")
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[0-9]', value):
            raise ValueError("Password must contain at least one number")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError("Password must contain at least one special character")
        # gensalt() generates a random cryptographic salt used to make each
        # hash unique, even if two users have the same password.
        self.__password = bcrypt.hashpw(value.encode('utf-8'),
                                        bcrypt.gensalt())

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.__password)
