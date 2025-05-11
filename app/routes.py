from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Movie, UserMovie
from sqlalchemy.orm import aliased
import requests
from config import Config

from app import application
from app import login_manager
from app import db
from forms import LoginForm, RegisterForm

from functions_for_routes import *

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
    form = LoginForm()
    
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials.', 'danger')
            return redirect(url_for('newlogin'))
    return render_template("redirectSignUp.html")

@application.route("/signup", methods=["GET"])
def signup():
    return render_template("signUp.html", underlined_tab_index=6)

@application.route("/signup_account", methods=["POST"])
def signup_account():
    form = RegisterForm()
    
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.', 'warning')
            return jsonify({'message': 'Username taken'}), 400

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully. You can now log in.', 'success')

    return jsonify({'message': 'Signup successful'}), 200

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
    
@application.route('/uploadReview')
@login_required
def uploadReview():

    movies = Movie.query.all()
    
    return render_template("uploadReview.html", api_key=Config.API_KEY, underlined_tab_index=2, movies = movies)

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
@application.route('/upload_movie', methods=['POST'])
@login_required
def upload_movie():
    try:
        data = request.get_json()
        title = data.get('movie_title')
        user_rating = data.get('user_rating')

        # Comment this lines of code when you want to add new movies to the database using the OMDB API Key.
        ###
        
        existing = Movie.query.filter_by(title=data.get('movie_title')).first()
        if not existing:
            print("Movie title doesnt exist. exiting submission")
            return jsonify({"error": f"Movie: {title} doesnt exist in database."}), 400
        
        ###
        # Uncomment this lines of code when you want to add new movies to the database using the OMDB API Key.
        ###
        """
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
        """
            
        existing_link = UserMovie.query.filter_by(user_id=current_user.id, movie_id=existing.id).first()

        if existing_link:
            existing_link.user_rating = user_rating
            message = f"Movie: {title} rating updated!"
        else:
            # Change existing to movie when you want to add movies to db using OMDB API Key
            user_movie = UserMovie(user_id=current_user.id, movie_id=existing.id, user_rating=user_rating)
            db.session.add(user_movie)
            message = f"Movie: {title} added to your list!"
        
        
        db.session.commit()
        return jsonify({"message": message}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to store movie: {str(e)}"}), 500
    
### ROUTE TO SEND API REQUEST TO AUTOCOMPLETE ###
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

@application.route('/search_movies', methods=['GET'])
def search_movies():
    search_query = request.args.get('q', '')
    
    # Query the database for users whose username contains the search query
    matching_movies = Movie.query.filter(Movie.title.ilike(f'%{search_query}%')).all()
    
    # Return a list of matching usernames
    return jsonify({"results": [movie.title for movie in matching_movies]})

@application.route('/shareData')
@login_required
def shareData():
    friended_by_list = []

    try:
        user = User.query.get(current_user.id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get all users who have added the current user as a friend
        friended_by_list = [
            {"id": u.id, "username": u.username}
            for u in user.friends_of.all()
        ]
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return render_template("shareData.html", underlined_tab_index=4, friends=friended_by_list)

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
    
    if current_user:
        if current_user.id != friend.id and not friend.is_friends_with(current_user):
            # Add the current user to the friend's friend list
            friend.friends.append(current_user)
            db.session.commit()
            return jsonify({"message": f"You were added as a friend to {friend.username}!"}), 200
        else:
            flash('Error, incorrect friend', 'warning')
            return jsonify({"error": "Cannot add yourself or already in their friend list!"}), 400
    else:
        return jsonify({"error": "User not found!"}), 404

@application.route('/visualiseMovies')
@login_required
def visualiseMovies():
    try:
        user_movie_alias = aliased(UserMovie)

        query = (
            db.session.query(
                Movie,
                user_movie_alias.user_rating  # pulls the current user's rating if exists
            )
            .join(  # innerjoin to only get rated movies
                user_movie_alias,
                (Movie.id == user_movie_alias.movie_id) & (user_movie_alias.user_id == current_user.id)
            )
            .filter(user_movie_alias.user_rating.isnot(None))  # Only movies with a rating
        )
        
        movies = query.all()
        
        movies_data = pack_movie_data_tuple(movies)

        return render_template("visualiseMovies.html", underlined_tab_index=3, movies = movies_data)
    except Exception as e:
        print("Could not get movies: " + str(e))
        return jsonify({"error": "Could not get movies", "details": str(e)}), 500

@application.route('/visualiseMoviesSuggested')
@login_required
def visualiseMoviesSuggested():
    try:
        user_movie_alias = aliased(UserMovie)

        movies = query_for_movies_rated(current_user).all()
        
        top_genre = calculate_top_genre(movies)

        all_movies = Movie.query.all()
        
        movies_of_genre = []
        movies_of_genre = get_movies_of_genre(all_movies, top_genre)

        movies_data = pack_movie_data_list(movies_of_genre)
            
        return render_template("visualiseMoviesSuggested.html", underlined_tab_index=3, movies=movies_data, top_genre=top_genre)
    except Exception as e:
        print("Could not get movies: " + str(e))
        return jsonify({"error": "Could not get movies", "details": str(e)}), 500


    
@application.route('/visualiseMoviesShared')
@login_required
def visualiseMoviesShared():

    movies_data = []
    friends_list = []

    try:
        user = User.query.get(current_user.id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        friends_list = [
            {"id": friend.id, "username": friend.username}
            for friend in user.friends
        ]

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    try:
        friend_username = request.args.get('friend_username', type=str)

        friend = User.query.filter_by(username=friend_username).first()

        movies = get_friend_movies(friend_username)
        
        # False means no friend is selected. And then renders the template with an empty friends list.
        if movies == False:
            return render_template("visualiseMoviesShared.html", underlined_tab_index=3, movies=movies_data, friends=friends_list)

        # Check if friend exists and if the current user is friends with the friend
        if not friend or not current_user.is_friends_with(friend):
            return jsonify({"error": "User is not friends with the specified friend"}), 403

        movies_data = pack_movie_data_tuple(movies)

    except Exception as e:
        print("Could not get movies: " + str(e))
        return jsonify({"error": "Could not get movies"}), 500
    
    return render_template("visualiseMoviesShared.html", underlined_tab_index=3, movies=movies_data, friends=friends_list)

@application.route('/visualiseMoviesSharedSuggested')
@login_required
def visualiseMoviesSharedSuggested():

    movies_data = []
    friends_list = []

    try:
        user = User.query.get(current_user.id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        friends_list = [
            {"id": friend.id, "username": friend.username}
            for friend in user.friends
        ]

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    try:
        friend_username = request.args.get('friend_username', type=str)

        movies = get_friend_movies(friend_username)
        if movies == False:
            return render_template("visualiseMoviesSharedSuggested.html", underlined_tab_index=3, movies=movies_data, friends=friends_list)
        
        top_genre = calculate_top_genre(movies)

        all_movies = Movie.query.all()
        
        movies_of_genre = []
        movies_of_genre = get_movies_of_genre(all_movies, top_genre)

        movies_of_genre = pack_movie_data_tuple(movies)

    except Exception as e:
        print("Could not get movies: " + str(e))
        return jsonify({"error": "Could not get movies"}), 500
    
    return render_template("visualiseMoviesSharedSuggested.html", underlined_tab_index=3, movies=movies_of_genre, friends=friends_list, top_genre=top_genre)

### The following code is profile ###

@application.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@application.route('/update_avatar_color', methods=['POST'])
@login_required
def update_avatar_color():
    try:
        data = request.get_json()
        color = data.get('color')
        
        if not color:
            return jsonify({'success': False, 'error': 'The color cannot be empty'}), 400
            
        # Update user avatar color
        current_user.avatar_color = color
        db.session.commit()
        
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@application.route('/update_bio', methods=['POST'])
@login_required
def update_bio():
    try:
        data = request.get_json()
        bio = data.get('bio', '')
        
        # Limit length
        if len(bio) > 500:
            bio = bio[:500]
            
        # Update user profile
        current_user.bio = bio
        db.session.commit()
        
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
### The above code is a profile ###
