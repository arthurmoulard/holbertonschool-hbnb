from app.models.BaseModel import BaseModel
from email_validator import validate_email, EmailNotValidError
from app import bcrypt


class User(BaseModel):
    def __init__(self, first_name, last_name, email,
                 password, is_admin=False):
        super().__init__()
        self.__first_name = None
        self.__last_name = None
        self.__email = None
        self.__password = None

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.reviews = []
        self.places = []

        # Hash fait UNE SEULE FOIS ici à la création
        self.hash_password(password)

    # ── Propriétés ───────────────────────────────────────────────────────────

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("first_name cannot be empty")
        if len(value) > 50:
            raise ValueError("first_name too long (max 50 chars)")
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("last_name cannot be empty")
        if len(value) > 50:
            raise ValueError("last_name too long (max 50 chars)")
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

    # ── Méthodes ─────────────────────────────────────────────────────────────

    def hash_password(self, password):
        """Hash le mot de passe en clair et le stocke."""
        if not password:
            raise ValueError("password cannot be empty")
        self.__password = bcrypt.generate_password_hash(
            password
        ).decode('utf-8')

    def verify_password(self, password):
        """Vérifie un mot de passe en clair contre le hash stocké."""
        return bcrypt.check_password_hash(self.__password, password)

    def update(self, data, is_admin=False):
        """
        Override de BaseModel.update().
        - Non-admin : ne peut pas modifier email ni password
        - Admin : peut tout modifier
        """
        PROTECTED = {'id', 'created_at', 'updated_at'}

        for key, value in data.items():
            if key in PROTECTED:
                continue
            if key in ('email', 'password') and not is_admin:
                raise ValueError("You cannot modify email or password.")
            if key == 'password':
                self.hash_password(value)
            elif hasattr(self, key):
                setattr(self, key, value)

        self.save()  # appelé UNE SEULE FOIS à la fin

    def add_review(self, review):
        self.reviews.append(review)

    def add_place(self, place):
        self.places.append(place)

    def to_dict(self):
        """Sérialisation sans le password."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        }