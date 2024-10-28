from application import app
from application.models import db,User


with app.app_context():
    db.create_all()

    admin = User.query.filter_by(role = 'admin').first()
    if not admin:
        new_admin = User(
            username = 'admin',
            email = 'admin@email.com',
            password = 'admin',
            role = 'admin'
        )
        db.session.add(new_admin)
        db.session.commit()

