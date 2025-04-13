from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Movie
from dotenv import load_dotenv
import os
import requests


app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
API_KEY = os.getenv("API_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdb.sqlite3'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials.', 'danger')
            return redirect(url_for('home'))
    return render_template("login.html")

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form['username']
    password = request.form['password']

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash('Username already exists.', 'warning')
        return redirect(url_for('login'))

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    flash('Account created successfully. You can now log in.', 'success')
    return redirect(url_for('login'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("home"))

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/uploadData')
@login_required
def uploadData():
    return render_template("uploadData.html", api_key=API_KEY)

@app.route('/fetch_movie', methods=['POST'])
@login_required
def fetch_movie():
    data = request.get_json()
    title = data.get("title")

    if not title:
        return jsonify({"error": "Missing movie title"}), 400

    import requests
    omdb_url = f"https://www.omdbapi.com/?t={title}&apikey={API_KEY}"
    response = requests.get(omdb_url)
    return jsonify(response.json())

@app.route('/shareData')
@login_required
def shareData():
    return render_template("shareData.html")

@app.route('/visualiseData')
@login_required
def visualiseData():
    return render_template("visualiseData.html")


if __name__ == '__main__':
    app.run(debug=True) 