from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Movie, UserMovie
from sqlalchemy.orm import aliased
from dotenv import load_dotenv
import os
import requests
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app import application
from app import login_manager

### The following code is a newly designed login/signup ###
@application.route("/newlogin")
def newlogin():
    return render_template("login_modal.html")

@application.route("/newsignup")
def newsignup():
    return render_template("signup_modal.html")

@application.route("/forgetPassword")
def forgetPassword():
    return render_template("forgetPassword_modal.html")
### The above code is a newly designed login/signup ###

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@application.route("/login", methods=["GET", "POST"])
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

@application.route("/signup", methods=["GET"])
def signup():
    return render_template("signUp.html", underlined_tab_index=6)

@application.route("/signup_account", methods=["POST"])
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

@application.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("home"))

@application.route('/')
def home():
    return render_template('index.html', underlined_tab_index=1)

@application.route('/loginModal')
def login_modal():
    return render_template('login_modal.html')
    
@application.route('/uploadData')
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
    
@application.route('/get_movies', methods=['GET'])
@login_required
def get_movies():
    try:
        """
        movies = (
            db.session.query(Movie)
            .join(UserMovie)
            .filter(UserMovie.user_id == current_user.id)
            .all()
        )"""

        user_movie_alias = aliased(UserMovie)

        query = (
            db.session.query(
                Movie,
                user_movie_alias.user_rating  # pulls the current user's rating if exists
            )
            .outerjoin(
                user_movie_alias,
                (Movie.id == user_movie_alias.movie_id) & (user_movie_alias.user_id == current_user.id)
            )
        )
        movies = query.all()
        
        movies_data = []
        for movie, user_rating in movies:
            movies_data.append({
                "title": movie.title,
                "year": movie.year,
                "rated": movie.rated,
                "released": movie.released,
                "genre": movie.genre,
                "director": movie.director,
                "writer" : movie.writer,
                "actors" : movie.actors,
                "imdb_rating" : movie.imdb_rating,
                "metascore" : movie.metascore,
                "box_office" : movie.box_office,
                "poster_url" : movie.poster_url,
                "user_rating" : user_rating
            })
        return jsonify({"movies": movies_data})
    except Exception as e:
        print("Could not get movies" + str(e))
        return jsonify("Could not get movies")
    
### ROUTE TO MAKE THE OMDB REQUEST, AND STORE THE RESPONSE IN THE DB ###
@application.route('/upload_movie', methods=['POST'])
@login_required
def submit_movie():
    try:
        data = request.get_json()
        title = data.get('movie_title')
        user_rating = data.get('user_rating')

        response = requests.get(f"https://www.omdbapi.com/?t={title}&apikey={Config.API_KEY}")
        movie_data = response.json()

        if movie_data.get("Response") == "False":
            return jsonify({"error": f"Movie: {title} not found"}), 404

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
                runtime=movie_data.get("Runtime"),
                genre=movie_data.get("Genre"),
                director=movie_data.get("Director"),
                writer=movie_data.get("Writer"),
                actors=movie_data.get("Actors", "Unknown"),
                language=movie_data.get("Language"),
                country=movie_data.get("Country"),
                imdb_rating=movie_data.get("imdbRating"),
                rt_rating=rt_rating,
                metascore=movie_data.get("Metascore"),
                box_office=movie_data.get("BoxOffice"),
                poster_url=movie_data.get("Poster")
            )
            db.session.add(movie)
            db.session.commit()
            
        existing_link = UserMovie.query.filter_by(user_id=current_user.id, movie_id=movie.id).first()

        if existing_link:
            existing_link.user_rating = user_rating
            message = f"Movie: {title} rating updated!"
        else:
            user_movie = UserMovie(user_id=current_user.id, movie_id=movie.id, user_rating=user_rating)
            db.session.add(user_movie)
            message = f"Movie: {title} added to your list!"
        
        
        db.session.commit()
        return jsonify({"message": message}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to store movie: {str(e)}"}), 500
    
### ROUTE FOR TO SEND API REQUEST TO AUTOCOMPLETE ###
@application.route("/autocomplete_movie")
@login_required
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


@application.route('/shareData')
@login_required
def shareData():
    return render_template("shareData.html", underlined_tab_index=4)

### Route to search for users/autcomplete in shareData.

@application.route('/search_users', methods=['GET'])
def search_users():
    search_query = request.args.get('q', '')
    
    # Query the database for users whose username contains the search query
    matching_users = User.query.filter(User.username.ilike(f'%{search_query}%')).all()
    
    # Return a list of matching usernames
    return jsonify([user.username for user in matching_users])

### Route to add friends username to DB.

@application.route('/add_friend', methods=['POST'])
@login_required
def add_friend():
    data = request.get_json()
    friend_username = data.get('username')

    # Check if the user exists in the database
    friend = User.query.filter_by(username=friend_username).first()
    
    if friend:
        # Add this user to the friend list
        if friend.id != current_user.id and not current_user.is_friends_with(friend):
            current_user.friends.append(friend)
            db.session.commit()
            return jsonify({"message": "Friend added!"}), 200
        else:
            return jsonify({"error": "Cannot add yourself or already friends!"}), 400
    else:
        return jsonify({"error": "User not found!"}), 404

@application.route('/visualiseData')
@login_required
def visualiseData():
    return render_template("visualiseData.html", underlined_tab_index=3)
