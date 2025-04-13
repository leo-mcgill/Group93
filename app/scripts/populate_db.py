import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import User, Movie

with app.app_context():
    #Just creating user for now
    user = User(username="testuser")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    
    
    #movie = Movie(title="Up", user_id=user.id)
    #db.session.add(movie)
    #db.session.commit()
    
    print("Test data added.")