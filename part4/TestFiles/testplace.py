import unittest
from app.api.v1 import create_app

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_place_success(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "Desc",
            "price": 50,
            "latitude": 10,
            "longitude": 20,
            "owner_id": "valid_user_id",
            "amenities": []
        })
        self.assertEqual(response.status_code, 201)

    def test_create_place_invalid_price(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Test",
            "description": "Desc",
            "price": -1,
            "latitude": 10,
            "longitude": 20,
            "owner_id": "valid_user_id",
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)

    def test_get_nonexistent_place(self):
        response = self.client.get('/api/v1/places/unknown')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
    