from flask import Flask
from flask_login import LoginManager

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

application = Flask(__name__)
application.config.from_object(Config)
db = SQLAlchemy(application)
migrate = Migrate(application, db)

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'login'

import routes

if __name__ == '__main__':
    application.run(debug=True) 


