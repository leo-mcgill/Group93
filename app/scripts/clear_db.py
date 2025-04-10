import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import User, Movie

with app.app_context():
    db.session.query(Movie).delete()
    db.session.query(User).delete()
    db.session.commit()
    print("All records deleted.")
    