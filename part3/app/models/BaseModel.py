import uuid
from datetime import datetime


class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Met à jour updated_at à chaque modification."""
        self.updated_at = datetime.now()

    def update(self, data, is_admin=False):
        """
        Met à jour les attributs depuis un dictionnaire.
        Les champs id, created_at, updated_at sont toujours protégés.
        """
        PROTECTED = {'id', 'created_at', 'updated_at'}

        for key, value in data.items():
            if key in PROTECTED:
                continue
            if hasattr(self, key):
                setattr(self, key, value)

        self.save()
        