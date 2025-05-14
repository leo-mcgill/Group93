#Group 93 CITS3403 Project 2025
#Configurations for the flask app.

import os

# Get the base directory of the app
basedir = os.path.abspath(os.path.dirname(__file__))

# Define the default location for the SQLite database inside the /instance folder
instance_folder = os.path.join(basedir, 'instance')
if not os.path.exists(instance_folder):
    os.makedirs(instance_folder)

default_database_location = 'sqlite:///' + os.path.join(instance_folder, 'yourdb.sqlite3')

class Config:
    # Use the environment variable DATABASE_URL or default to the local SQLite database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or default_database_location
    SECRET_KEY = os.getenv('SECRET_KEY')
    API_KEY = os.getenv('API_KEY')
