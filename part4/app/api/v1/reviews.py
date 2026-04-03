from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
    # user_id absent — forcé depuis le token JWT
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Create a new review (authenticated users only)"""
        current_user_id = get_jwt_identity()
        data = api.payload

        place = facade.get_place(data.get('place_id'))
        if not place:
            return {'error': 'Place not found'}, 404

        # Ne peut pas reviewer sa propre place
        if place.owner_id == current_user_id:
            return {'error': 'You cannot review your own place.'}, 400

        # Ne peut reviewer qu'une seule fois par place
        existing = facade.get_reviews_by_place(data['place_id'])
        if any(r.user.id == current_user_id for r in existing):
            return {'error': 'You have already reviewed this place.'}, 400

        # user_id forcé depuis le token
        data['user_id'] = current_user_id

        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews (public)"""
        return [r.to_dict() for r in facade.get_all_reviews()], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID (public)"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @jwt_required()
    def put(self, review_id):
        """Update a review (author only — admin bypasses via /admin/reviews/)"""
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin and review.user.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            updated = facade.update_review(review_id, api.payload)
            return updated.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (author only — admin bypasses via /admin/reviews/)"""
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin and review.user.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200