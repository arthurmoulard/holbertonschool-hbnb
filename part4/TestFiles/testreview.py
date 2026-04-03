import unittest
from app import create_app


class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_get_review_not_found(self):
        response = self.client.get('/api/v1/reviews/non_existing_id')
        self.assertEqual(response.status_code, 404)

    def test_delete_review_not_found(self):
        response = self.client.delete('/api/v1/reviews/non_existing_id')
        self.assertEqual(response.status_code, 404)

    def test_create_review_invalid_rating(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Nice place",
            "rating": 10,
            "user_id": "fake_user",
            "place_id": "fake_place"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_empty_text(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 3,
            "user_id": "fake_user",
            "place_id": "fake_place"
        })
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()