# Group93
Agile Web Development project created by Group 93

Instructions to run Flask application
1: create a python virtual environment (Only need to do this once)
2: activate your virtual environment
3: install requirements on your virtual environments
4: initialise your local DB
5: run the flask application



1: Create python virtual environment (Only need to do this once):
$ python -m venv venv

2: Activate your virtual environment:
$ source venv/bin/activate # macOS/Linux
$ venv\scripts\acticate # Windows

3: Install requirements on Venv (only need to do this once):
$ pip install -r requirements.txt

--- DATABASE ---

There are three scripts to handle your local DB.

4: Initialise the DB:
$ python scripts/init_db.py

Populate the DB for testing:
$ python scripts/populate_db.py

Clear all entries from the DB:
$ python scripts/clear_db.py

5: run the app:
$ python app.py

6: open your browser and go to:
http://127.0.0.1:5000/

To quit:
ctrl + c in terminal

Make sure to leave your virtual environment once you want to commit or pull/push:
$ deactivate

May need to cd into Group93 to activate venv depending on where you create it.s