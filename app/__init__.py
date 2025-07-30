from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import db
from .routes import main

login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(main)
    return app
