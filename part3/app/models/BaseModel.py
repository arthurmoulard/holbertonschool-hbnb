from app import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    # SQLAlchemy ne crée pas de table pour cette classe
    __abstract__ = True

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def save(self):
        """Met à jour updated_at et commit en base."""
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def update(self, data, is_admin=False):
        """Met à jour les attributs depuis un dictionnaire."""
        PROTECTED = {'id', 'created_at', 'updated_at'}

        for key, value in data.items():
            if key in PROTECTED:
                continue
            if hasattr(self, key):
                setattr(self, key, value)

        self.save()