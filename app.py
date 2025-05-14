#Group 93 CITS3403 Project 2025
# Main start point for the flask application.
from app import create_app
from app import Config

application = create_app(Config)

if __name__ == '__main__':
    application.run(debug=True)

