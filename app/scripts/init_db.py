#Group 93 CITS3403 Project 2025
#script to create db and tables

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import application, db
# from app.models import User, Movie  # ensure correct import path

from sqlalchemy import inspect

with application.app_context():
    db.create_all()
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print("Database tables:")
    print(tables)
    print("Database initialized.")
