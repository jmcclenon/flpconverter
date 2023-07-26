from flask import Flask
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    # Secret key for CSRF protection
    app.config['SECRET_KEY'] = '3b3533dacf63f08d6fa69d8e36c89cxx'

    # Import and register blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
