from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Movie
from dotenv import load_dotenv
import os


app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

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
def uploadData():
    return render_template("uploadData.html")

@app.route('/shareData')
def shareData():
    return render_template("shareData.html")

@app.route('/visualiseData')
def visualiseData():
    return render_template("visualiseData.html")


if __name__ == '__main__':
    app.run(debug=True)