import os
from app import create_app
from app.services import facade

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Crée un admin par défaut si aucun n'existe
        if not facade.get_user_by_email('admin@hbnb.io'):
            facade.create_user({
                'first_name': 'Admin',
                'last_name': 'HBnB',
                'email': 'admin@hbnb.io',
                'password': os.getenv('ADMIN_PASSWORD', 'admin1234'),
                'is_admin': True
            })
    app.run(debug=app.config['DEBUG'])
    