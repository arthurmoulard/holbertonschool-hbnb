import os
from app import create_app, db
from app.services import facade

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Crée toutes les tables
        db.create_all()

        # Crée l'admin par défaut si inexistant
        if not facade.get_user_by_email('admin@hbnb.io'):
            facade.create_user({
                'first_name': 'Admin',
                'last_name': 'HBnB',
                'email': 'admin@hbnb.io',
                'password': os.getenv('ADMIN_PASSWORD', 'admin1234'),
                'is_admin': True
            })
            print("Admin créé : admin@hbnb.io / admin1234")

    app.run(debug=app.config['DEBUG'])