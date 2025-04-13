#py script to remove all entries from all movie table

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import User, Movie

with app.app_context():
    db.session.query(Movie).delete()
    db.session.commit()
    print("All movies deleted.")