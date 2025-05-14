#Group 93 CITS3403 Project 2025
#script to remove all data from movie table

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import application, db
from models import User, Movie

with application.app_context():
    db.session.query(Movie).delete()
    db.session.commit()
    print("All movies deleted.")
