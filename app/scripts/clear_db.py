#Group 93 CITS3403 Project 2025
#script to remove all data from Movie, and User

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

application = create_app()
from app.models import User, Movie

with application.app_context():
    db.session.query(Movie).delete()
    db.session.query(User).delete()
    db.session.commit()
    print("All records deleted.")
    
