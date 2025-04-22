# Group93  
Agile Web Development project created by Group 93  

Instructions to run Flask application  
1: create a python virtual environment (Only need to do this once)  
2: activate your virtual environment  
3: upgrade pip to the latest version  
4: install requirements on your virtual environments  
5: initialise your local DB  
6: run the flask application  



1: Create python virtual environment (Only need to do this once):  
$ python -m venv venv  

2: Activate your virtual environment:  
$ source venv/bin/activate # macOS/Linux  
$ .\venv\Scripts\Activate.ps1 # Windows  

If you encounter the following error on Windows:  
.\venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.  

Please run PowerShell as Administrator (press Win + X → choose Windows PowerShell (Admin)), and enter the following command:  
$ set-executionpolicy remotesigned  
Then type Y and press Enter to confirm.  

To verify if the change was successful, run:  
$ get-executionpolicy  
If the output is 'RemoteSigned', the policy has been updated successfully.  

3. Upgrade pip to the latest version  
$ python.exe -m pip install --upgrade pip  

--- Before continuing, make sure your terminal is in the app directory (cd app) ---  

4: Install requirements on Venv (only need to do this once):  
$ pip install -r requirements.txt  

--- DATABASE ---  

There are three scripts to handle your local DB.  

5: Initialise the DB:  
$ python scripts/init_db.py  

Populate the DB for testing:  
$ python scripts/populate_db.py  

Clear all entries from the DB:  
$ python scripts/clear_db.py  

5: run the app:  
$ python app.py  

6: open your browser and go to:  
http://127.0.0.1:5000/  

7: create a .env file in /app    
add to .env file: SECRET_KEY = "example_secret_key"  

To quit:  
ctrl + c in terminal  

Make sure to leave your virtual environment once you want to commit or pull/push:  
$ deactivate  

May need to cd into Group93 to activate venv depending on where you create it.s  
