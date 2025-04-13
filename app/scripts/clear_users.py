#py script to remove all users from user table

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import User

with app.app_context():
    db.session.query(User).delete()
    db.session.commit()
    print("All users deleted.")