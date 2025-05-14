from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import Config, TestingConfig

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class = Config):
    # Create and configure the Flask app
    application = Flask(__name__, static_folder='static')
    application.config.from_object(config_class)
    
    # Initialize extensions with the app
    db.init_app(application)
    migrate.init_app(application, db)
    login_manager.init_app(application)
    login_manager.login_view = 'login'
    
    # Import and register routes
    with application.app_context():
        import app.routes  # Import the routes after the app is created
        app.routes.init_routes(application)
    
    return application