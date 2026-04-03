from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('admin', description='Admin operations')

# ── Models ───────────────────────────────────────────────────────────────────

user_model = api.model('AdminUser', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

user_update_model = api.model('AdminUserUpdate', {
    'first_name': fields.String(),
    'last_name': fields.String(),
    'email': fields.String(),
    'password': fields.String()
})

amenity_model = api.model('AdminAmenity', {
    'name': fields.String(required=True)
})

place_model = api.model('AdminPlace', {
    'title': fields.String(),
    'description': fields.String(),
    'price': fields.Float(),
    'latitude': fields.Float(),
    'longitude': fields.Float()
})

review_model = api.model('AdminReview', {
    'text': fields.String(),
    'rating': fields.Integer()
})

# ── Helper ───────────────────────────────────────────────────────────────────


def check_admin():
    """
    Lit is_admin directement dans le token JWT.
    Retourne (True, None) si admin, (False, response) sinon.
    """
    if not get_jwt().get('is_admin', False):
        return False, ({'error': 'Admin privileges required'}, 403)
    return True, None

# ── Users ────────────────────────────────────────────────────────────────────


@api.route('/users/')
class AdminUserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Admin — Create a new user (can set is_admin)"""
        ok, err = check_admin()
        if not ok:
            return err

        data = api.payload
        if facade.get_user_by_email(data['email']):
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(data)
            return new_user.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Email already in use')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Admin — Update any user (email and password included)"""
        ok, err = check_admin()
        if not ok:
            return err

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        new_email = api.payload.get('email')
        if new_email and new_email != user.email:
            if facade.get_user_by_email(new_email):
                return {'error': 'Email already in use'}, 400

        try:
            updated = facade.update_user(user_id, api.payload, is_admin=True)
            return updated.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

# ── Amenities ────────────────────────────────────────────────────────────────


@api.route('/amenities/')
class AdminAmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Admin — Create a new amenity"""
        ok, err = check_admin()
        if not ok:
            return err
        try:
            amenity = facade.create_amenity(api.payload)
            return amenity.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/amenities/<amenity_id>')
class AdminAmenityResource(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def put(self, amenity_id):
        """Admin — Update an amenity"""
        ok, err = check_admin()
        if not ok:
            return err
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        try:
            updated = facade.update_amenity(amenity_id, api.payload)
            return updated.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

# ── Places ───────────────────────────────────────────────────────────────────


@api.route('/places/<place_id>')
class AdminPlaceResource(Resource):
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Place not found')
    @jwt_required()
    def put(self, place_id):
        """Admin — Update any place (ownership bypassed)"""
        ok, err = check_admin()
        if not ok:
            return err
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        try:
            updated = facade.update_place(place_id, api.payload)
            return updated.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Place deleted successfully')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Place not found')
    @jwt_required()
    def delete(self, place_id):
        """Admin — Delete any place (ownership bypassed)"""
        ok, err = check_admin()
        if not ok:
            return err
        try:
            facade.delete_place(place_id)
            return {'message': 'Place deleted successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 404

# ── Reviews ──────────────────────────────────────────────────────────────────


@api.route('/reviews/<review_id>')
class AdminReviewResource(Resource):
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Review not found')
    @jwt_required()
    def put(self, review_id):
        """Admin — Update any review (ownership bypassed)"""
        ok, err = check_admin()
        if not ok:
            return err
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        try:
            updated = facade.update_review(review_id, api.payload)
            return updated.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Admin — Delete any review (ownership bypassed)"""
        ok, err = check_admin()
        if not ok:
            return err
        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 404
