from app.models.basemodel import BaseModel as BaseModel
from email_validator import validate_email, EmailNotValidError


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

    def __init__(self, first_name, last_name, email):
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
            raise ValueError
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
            raise ValueError
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
            raise ValueError

        try:
            valid = validate_email(value)
            self.__email = valid.normalized
        except EmailNotValidError:
            raise ValueError("Invalid email address format")

        self.__email = value

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
