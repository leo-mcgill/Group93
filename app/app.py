from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Movie, UserMovie
from dotenv import load_dotenv
import os
import requests
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

### The following code is a newly designed login/signup ###
@app.route("/newlogin")
def newlogin():
    return render_template("login_modal.html")

@app.route("/newsignup")
def newsignup():
    return render_template("signup_modal.html")

@app.route("/forgetPassword")
def forgetPassword():
    return render_template("forgetPassword_modal.html")
### The above code is a newly designed login/signup ###

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
    return render_template("redirectSignUp.html")

@app.route("/signup", methods=["GET"])
def signup():
    return render_template("signUp.html", underlined_tab_index=6)

@app.route("/signup_account", methods=["POST"])
def signup_account():
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
    return redirect(url_for('home'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("home"))

@app.route('/')
def home():
    return render_template('index.html', underlined_tab_index=1)

@app.route('/loginModal')
def login_modal():
    return render_template('login_modal.html')
    
@app.route('/uploadData')
@login_required
def uploadData():
    return render_template("uploadData.html", api_key=Config.API_KEY, underlined_tab_index=2)

### Methods to handle N/A responses from OMDB ###
def safe_float(val, default=None):
    try:
        return float(val) if val not in [None, "N/A"] else default
    except:
        return default

def safe_int(val, default=None):
    try:
        return int(val) if val not in [None, "N/A"] else default
    except:
        return default

### ROUTE TO MAKE THE OMDB REQUEST, AND STORE THE RESPONSE IN THE DB ###

@app.route('/fetch_movie', methods=['POST'])
@login_required
def fetch_movie():
    try:
        data = request.get_json()
        title = data.get('movie_title')
        user_rating = data.get('user_rating')

        response = requests.get(f"https://www.omdbapi.com/?t={title}&apikey={api_key}")
        movie_data = response.json()

        if movie_data.get("Response") == "False":
            return jsonify({"error": "Movie not found"}), 404

        # Safely extract fields
        runtime_str = movie_data.get("Runtime", "0").replace(" min", "")
        runtime = safe_int(runtime_str, default=0)

        imdb_rating = safe_float(movie_data.get("imdbRating"))
        metascore = safe_int(movie_data.get("Metascore"))
        rt_rating = (
            movie_data.get("Ratings", [{}])[1].get("Value")
            if len(movie_data.get("Ratings", [])) > 1
            else None
        )
        
        
        movie = Movie.query.filter_by(
            title=movie_data.get("Title", "Unknown"),
            year=movie_data.get("Year")).first()
        
        
        if not movie:
            movie = Movie(
                title=movie_data.get("Title", "Unknown"),
                year=movie_data.get("Year"),
                rated=movie_data.get("Rated"),
                released=movie_data.get("Released"),
                runtime=runtime,
                genre=movie_data.get("Genre"),
                director=movie_data.get("Director"),
                writer=movie_data.get("Writer"),
                actors=movie_data.get("Actors", "Unknown"),
                language=movie_data.get("Language"),
                country=movie_data.get("Country"),
                imdb_rating=imdb_rating,
                rt_rating=rt_rating,
                metascore=metascore,
                box_office=movie_data.get("BoxOffice")
            )
            db.session.add(movie)
            db.session.commit()
            
        existing_link = UserMovie.query.filter_by(user_id=current_user.id, movie_id=movie.id).first()

        if existing_link:
            existing_link.user_rating = user_rating
            message = "Movie rating updated!"
        else:
            user_movie = UserMovie(user_id=current_user.id, movie_id=movie.id, user_rating=user_rating)
            db.session.add(user_movie)
            message = "Movie added to your list!"
        
        
        db.session.commit()
        return jsonify({"message": message}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to store movie: {str(e)}"}), 500

### ROUTE FOR TO SEND API REQUEST TO AUTOCOMPLETE ###

@app.route("/autocomplete_movie")
def autocomplete_movie():
    query = request.args.get('q', '')  # Get the query string from the request
    if not query:
        return jsonify({'error': 'No query parameter provided'}), 400

    # Call the OMDB API or use another service to get movie suggestions
    response = requests.get(f"http://www.omdbapi.com/?s={query}&apikey={Config.API_KEY}")
    
    # Check if the response is valid and contains movie results
    if response.status_code == 200:
        data = response.json()
        if 'Search' in data:
            movies = [movie['Title'] for movie in data['Search']]
            return jsonify({'results': movies})  # Send movie titles as the response
        else:
            return jsonify({'results': []})  # No results found
    else:
        return jsonify({'error': 'Failed to fetch data from OMDB API'}), 500


@app.route('/shareData')
@login_required
def shareData():
    return render_template("shareData.html", underlined_tab_index=4)

@app.route('/visualiseData')
@login_required
def visualiseData():
    return render_template("visualiseData.html", underlined_tab_index=3)


if __name__ == '__main__':
    app.run(debug=True) 
