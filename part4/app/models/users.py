from app import db, bcrypt
from app.models.BaseModel import BaseModel
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.orm import validates


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # Relations définies dans Place et Review via backref
    # user.places et user.reviews disponibles automatiquement

    @validates('first_name')
    def validate_first_name(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("first_name cannot be empty")
        if len(value) > 50:
            raise ValueError("first_name too long (max 50 chars)")
        return value

    @validates('last_name')
    def validate_last_name(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("last_name cannot be empty")
        if len(value) > 50:
            raise ValueError("last_name too long (max 50 chars)")
        return value

    @validates('email')
    def validate_email(self, key, value):
        if not value:
            raise ValueError("email cannot be empty")
        try:
            valid = validate_email(value, check_deliverability=False)
            return valid.normalized
        except EmailNotValidError:
            raise ValueError("Invalid email address format")

    def hash_password(self, password):
        """Hash le mot de passe et le stocke."""
        if not password:
            raise ValueError("password cannot be empty")
        self.password = bcrypt.generate_password_hash(
            password
        ).decode('utf-8')

    def verify_password(self, password):
        """Vérifie le mot de passe contre le hash stocké."""
        return bcrypt.check_password_hash(self.password, password)

    def update(self, data, is_admin=False):
        """Override avec gestion des champs sensibles."""
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

        self.save()

    def to_dict(self):
        """Sérialisation sans le password."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        }
