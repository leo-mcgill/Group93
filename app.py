#Group 93 CITS3403 Project 2025
# Main start point for the flask application.
from app import create_app

application = create_app()

if __name__ == '__main__':
    application.run(debug=True)

