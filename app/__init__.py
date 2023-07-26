from flask import Flask
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    # Secret key for CSRF protection
    app.config['SECRET_KEY'] = 'Your secret key'

    # Import and register blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
