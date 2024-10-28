from flask import Flask
from application.models import db


def create_app():
    app = Flask(
        __name__,
        static_folder='../static',
        template_folder='../templates'
        )
    app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///library.sqlite3"
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config['SECRET_KEY']='this is mad1 session'

    db.init_app(app)
    with app.app_context():
        import application.views
        import application.views_user
        import application.views_admin
    return app

app = create_app()


