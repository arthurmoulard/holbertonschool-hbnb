import unittest
from app import create_app


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_create_user(self):
        """Test création d'un utilisateur valide"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid(self):
        """Test création utilisateur avec données invalides"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_user_not_found(self):
        """Test récupération utilisateur inexistant"""
        response = self.client.get('/api/v1/users/non_existing_id')
        self.assertEqual(response.status_code, 404)

    def test_update_user_not_found(self):
        """Test update utilisateur inexistant"""
        response = self.client.put('/api/v1/users/non_existing_id', json={
            "first_name": "Ghost",
            "last_name": "User",
            "email": "ghost@example.com"
        })
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()