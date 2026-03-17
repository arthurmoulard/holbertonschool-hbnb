from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password')
})

# email et password absents — non modifiables par un user normal
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid data')
    def post(self):
        """Register a new user (auto-inscription, is_admin toujours False)"""
        user_data = api.payload

        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400

        # Sécurité — on force is_admin à False
        # seul l'admin peut créer des admins via /api/v1/admin/users/
        user_data['is_admin'] = False

        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        return [u.to_dict() for u in facade.get_all_user()], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update user (first_name, last_name only — own account)"""
        current_user_id = get_jwt_identity()

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if user.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            updated = facade.update_user(user_id, api.payload, is_admin=False)
            return updated.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
        