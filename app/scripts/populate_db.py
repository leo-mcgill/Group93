#Group 93 CITS3403 Project 2025
#script to add test data.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import application, db
from models import User, Movie

with application.app_context():
    #Just creating user for now
    user = User(username="testuser")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    
    #movie = Movie(title="Up", user_id=user.id)
    #db.session.add(movie)
    #db.session.commit()
    
    print("Test user added.")
