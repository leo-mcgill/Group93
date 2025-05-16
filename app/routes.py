#Group 93 CITS3403 Project 2025
#routes file for all routes used by flask app

from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Movie, UserMovie
from sqlalchemy.orm import aliased
import requests
from app.config import Config
from collections import Counter

from app import login_manager, db
from app.forms import LoginForm, RegisterForm
from app.functions_for_routes import *

def init_routes(application):

    @application.route("/newlogin")
    def newlogin():
        return render_template("login_modal.html")

    @application.route("/newsignup")
    def newsignup():
        return render_template("signup_modal.html")

    @application.route("/forgetPassword")
    def forgetPassword():
        return render_template("forgetPassword_modal.html")

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

    @application.route("/signup_account", methods=["POST"])
    def signup_account():
        form = RegisterForm()
        
        if request.method == 'POST':
            username = form.username.data
            password = form.password.data
            confirmPassword = request.form.get('confirm_password')

            if password != confirmPassword:
                flash("Password do not match.Please try again..", 'warning')
                return jsonify({'message':'Password do not match'})
            
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

            # This checks if the movie exists in the database and if not, returns an error
            existing = Movie.query.filter_by(title=data.get('movie_title')).first()
            if not existing:
                print("Movie title doesnt exist. exiting submission")
                return jsonify({"error": f"Movie: {title} doesnt exist in database."}), 400        

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
        
        # Query the database for movies whose title contains the search query
        matching_movies = Movie.query.filter(Movie.title.ilike(f'%{search_query}%')).all()
        
        # Return a list of matching movies
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


    @application.route('/unshare_with_user', methods=['POST'])
    @login_required
    def remove_friend():
        try:
            data = request.get_json()
            friend_username = data.get('username')

            if not friend_username:
                return jsonify({"error": "Username cannot be empty"}), 400
            
            # Check if the user exists
            friend = User.query.filter_by(username=friend_username).first()
            
            if not friend:
                return jsonify({"error": "The user does not exist"}), 404
            
            # Check if are a friend
            if not friend.is_friends_with(current_user):
                return jsonify({"error": "This user is not in your share list"}), 400
            
            # Remove from the friend list
            friend.friends.remove(current_user)
            db.session.commit()

            return jsonify({"message": f"You have stopped sharing your data with {friend.username}"}), 200
        except Exception as e:
            db.session.rollback()  # Roll back the database transaction when an exception occurs
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    @application.route('/share_with_user', methods=['POST'])
    @login_required
    def share_with_user():
        try:
            data = request.get_json()
            friend_username = data.get('username')

            if not friend_username:
                return jsonify({"error": "Username cannot be empty"}), 400

        # Check if the user exists in the database
            friend = User.query.filter_by(username=friend_username).first()

            if not friend:
                return jsonify({"error": "User not found"}), 404

            # Cannot add yourself as a friend
            if current_user.id == friend.id:
                return jsonify({"error": "Cannot add yourself as a friend"}), 400

            # Check if already friends
            if friend.is_friends_with(current_user):
                return jsonify({"error": "Already in their friend list"}), 400

            # Add the current user to the friend's friend list
            friend.friends.append(current_user)
            db.session.commit()

            return jsonify({"message": f"You were added as a friend to {friend.username}!"}), 200
        except Exception as e:
            db.session.rollback()  # Roll back the database transaction in case of an exception.
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    # This function queries for movies that the user has rated and returns data about each movie.
    @application.route('/visualiseMovies')
    @login_required
    def visualiseMovies():
        try:
            user_movie_alias = aliased(UserMovie)

            query = (
                db.session.query(
                    Movie,
                    user_movie_alias.user_rating
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

    # This function queries for the top genre based on the current movie ratings. It returns a list of all movies of that specific genre from the database.
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

    # This route returns all the movies that have been rated by a friend.
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

            movies = get_friend_movies(current_user, friend_username)
            
            # False means no friend is selected. And then renders the template with an empty friends list.
            if movies == False:
                return render_template("visualiseMoviesShared.html", underlined_tab_index=3, movies=movies_data, friends=friends_list)

            # If friend doesnt exist or if the current user is friends with the friend then return an error
            if not friend or not current_user.is_friends_with(friend):
                return jsonify({"error": "User is not friends with the specified friend"}), 403

            movies_data = pack_movie_data_tuple(movies)

        except Exception as e:
            print("Could not get movies: " + str(e))
            return jsonify({"error": "Could not get movies"}), 500
        
        return render_template("visualiseMoviesShared.html", underlined_tab_index=3, movies=movies_data, friends=friends_list)

    # This route gets the top genre of a friend based on the ratings of that friend and returns all movies in that genre.
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

            movies = get_friend_movies(current_user, friend_username)
            if movies == False:
                return render_template("visualiseMoviesSharedSuggested.html", underlined_tab_index=3, movies=movies_data, friends=friends_list)
            
            top_genre = calculate_top_genre(movies)

            all_movies = Movie.query.all()
            
            movies_of_genre = []
            movies_of_genre = get_movies_of_genre(all_movies, top_genre)
            
            movies_of_genre = pack_movie_data_list(movies_of_genre)

        except Exception as e:
            print("Could not get movies: " + str(e))
            return jsonify({"error": "Could not get movies"}), 500
        
        return render_template("visualiseMoviesSharedSuggested.html", underlined_tab_index=3, movies=movies_of_genre, friends=friends_list, top_genre=top_genre)

    ### Route to show user movie stats ###
    @application.route('/visualiseMoviesStatistics')
    @login_required
    def visualiseMoviesStatistics():
        # Query total runtime of all movies watched by the user
        total_runtime = db.session.query(db.func.sum(Movie.runtime)).join(UserMovie).filter(UserMovie.user_id == current_user.id).scalar() or 0
        
        # Query all movies the user has watched (with actors and genres as comma-separated strings)
        user_movies = db.session.query(Movie.actors, Movie.genre).join(UserMovie).filter(UserMovie.user_id == current_user.id).all()

        # Process the actors data and count their occurrences
        actor_list = []
        genre_list = []  # Create a list to store genres
        for movie in user_movies:
            # Split the actors by commas and strip any leading/trailing whitespace
            actors = [actor.strip() for actor in movie.actors.split(',')]
            actor_list.extend(actors)
            
            # Split the genres by commas and strip any leading/trailing whitespace
            genres = [genre.strip() for genre in movie.genre.split(',')]
            genre_list.extend(genres)

        # Count the most common actors
        actor_counts = Counter(actor_list)
        top_actors = actor_counts.most_common(3)

        # Count the most common genres
        genre_counts = Counter(genre_list)
        top_genres = genre_counts.most_common(3)

        # Query the most watched genres
        genres_count = db.session.query(Movie.genre, db.func.count(Movie.id).label('count')).join(UserMovie).filter(UserMovie.user_id == current_user.id).group_by(Movie.genre).order_by(db.desc('count')).limit(5).all()

        # Calculate the genre diversity score
        total_movies = Movie.query.join(UserMovie).filter(UserMovie.user_id == current_user.id).count()
        unique_genres = db.session.query(db.func.count(db.distinct(Movie.genre))).join(UserMovie).filter(UserMovie.user_id == current_user.id).scalar() or 0
        genre_diversity_score = (unique_genres / total_movies) * 100 if total_movies > 0 else 0
        genre_diversity_score = round(genre_diversity_score,2)
        # Query the user's 3 highest rated movies
        top_rated_movies = db.session.query(Movie.title, UserMovie.user_rating).join(UserMovie).filter(UserMovie.user_id == current_user.id).order_by(db.desc(UserMovie.user_rating)).limit(3).all()

        # Calculate top-genre engagement score
        most_watched_genre = db.session.query(Movie.genre, db.func.count(Movie.id).label('count')).join(UserMovie).filter(UserMovie.user_id == current_user.id).group_by(Movie.genre).order_by(db.desc('count')).first()
        if most_watched_genre:
            most_watched_genre_count = most_watched_genre[1]
            genre_engagement_score = db.session.query(db.func.avg(UserMovie.user_rating)).join(Movie).filter(Movie.genre == most_watched_genre[0], UserMovie.user_id == current_user.id).scalar() or 0
            top_genre_engagement_score = most_watched_genre_count * genre_engagement_score
            top_genre_engagement_score = round(top_genre_engagement_score,2)
        else:
            top_genre_engagement_score = 0

        # Render the statistics page with the gathered data
        return render_template('visualiseMoviesStatistics.html',
                            underlined_tab_index=3,
                            total_runtime=total_runtime,
                            top_actors=top_actors,  # Pass the top actors to the template
                            top_genres=top_genres,  # Pass the top genres to the template
                            genres_count=genres_count,
                            genre_diversity_score=genre_diversity_score,
                            top_rated_movies=top_rated_movies,
                            top_genre_engagement_score=top_genre_engagement_score)
        
    # this route gets statistics of the rated movies of a friend.
    @application.route('/visualiseMoviesSharedStatistics', methods=['GET', 'POST'])
    @login_required
    def visualiseMoviesSharedStatistics():
        # Get the friend's username from the query parameter
        friend_username = request.args.get('friend_username')

        # Fetch the list of friends for the user
        friends = current_user.friends

        if friend_username:
            # Fetch the friend's user object
            friend = User.query.filter_by(username=friend_username).first()
            if not friend:
                flash("Friend not found.", "danger")
                return redirect(url_for('home'))

            # Query all movies that the friend has watched (with actors and genres as comma-separated strings)
            user_movies = db.session.query(Movie.actors, Movie.genre).join(UserMovie).filter(UserMovie.user_id == friend.id).all()
        
            total_runtime = db.session.query(db.func.sum(Movie.runtime)).join(UserMovie).filter(UserMovie.user_id == friend.id).scalar() or 0

        else:
            # If no friend is selected, don't load the statistics section yet
            return render_template('visualiseMoviesSharedStatistics.html', underlined_tab_index=3, friends=friends, friend=None)

        # Process the friend’s movie data (same logic as the user's)
        actor_list = []
        genre_list = []
        for movie in user_movies:
            actors = [actor.strip() for actor in movie.actors.split(',')]
            actor_list.extend(actors)

            genres = [genre.strip() for genre in movie.genre.split(',')]
            genre_list.extend(genres)

        # Count the most common actors and genres for the friend
        actor_counts = Counter(actor_list)
        top_actors = actor_counts.most_common(3)

        genre_counts = Counter(genre_list)
        top_genres = genre_counts.most_common(3)

        # Query the most watched genres
        genres_count = db.session.query(Movie.genre, db.func.count(Movie.id).label('count')).join(UserMovie).filter(UserMovie.user_id == friend.id).group_by(Movie.genre).order_by(db.desc('count')).limit(5).all()

        # Calculate the genre diversity score for the friend
        total_movies = Movie.query.join(UserMovie).filter(UserMovie.user_id == friend.id).count()
        unique_genres = db.session.query(db.func.count(db.distinct(Movie.genre))).join(UserMovie).filter(UserMovie.user_id == friend.id).scalar() or 0
        genre_diversity_score = (unique_genres / total_movies) * 100 if total_movies > 0 else 0

        # Query the friend's top 3 highest rated movies
        top_rated_movies = db.session.query(Movie.title, UserMovie.user_rating).join(UserMovie).filter(UserMovie.user_id == friend.id).order_by(db.desc(UserMovie.user_rating)).limit(3).all()

        # Calculate top-genre engagement score for the friend
        most_watched_genre = db.session.query(Movie.genre, db.func.count(Movie.id).label('count')).join(UserMovie).filter(UserMovie.user_id == friend.id).group_by(Movie.genre).order_by(db.desc('count')).first()
        if most_watched_genre:
            most_watched_genre_count = most_watched_genre[1]
            genre_engagement_score = db.session.query(db.func.avg(UserMovie.user_rating)).join(Movie).filter(Movie.genre == most_watched_genre[0], UserMovie.user_id == friend.id).scalar() or 0
            top_genre_engagement_score = most_watched_genre_count * genre_engagement_score
        else:
            top_genre_engagement_score = 0

        # Render the statistics page for the friend's data
        return render_template('visualiseMoviesSharedStatistics.html',
                            underlined_tab_index=3,
                            friends=friends,
                            friend=friend,
                            total_runtime=total_runtime,
                            top_actors=top_actors,
                            top_genres=top_genres,
                            genres_count=genres_count,
                            genre_diversity_score=genre_diversity_score,
                            top_rated_movies=top_rated_movies,
                            top_genre_engagement_score=top_genre_engagement_score)

    @application.route("/profile")
    @login_required
    def profile():
        # Get the username in the query parameters
        username = request.args.get('username')

        # If the username is not provided or the username is currently logged in, the current user's profile will be displayed.
        if not username or username == current_user.username:
            profile_user = current_user
            is_own_profile = True
        else:
            # Find the requested user
            profile_user = User.query.filter_by(username=username).first()
            # If the user does not exist, redirect to the current user's profile
            if not profile_user:
                flash("User not found", "error")
                return redirect(url_for('profile'))
            
            is_own_profile = False
        
        # Get movie collection data
        favorite_movies = get_favorite_movies(profile_user.id)
        movie_stats = get_movie_stats(profile_user.id)

        users_friended_by_current = db.session.query(User).join(
            user_friends, user_friends.c.user_id == User.id
        ).filter(
            user_friends.c.friend_id == profile_user.id
        ).all()

        return render_template("profile.html", 
                            profile_user=profile_user, 
                            friends=users_friended_by_current,
                            is_own_profile=is_own_profile,
                            favorite_movies=favorite_movies,
                            movie_stats=movie_stats)

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
        
    # User search route
    @application.route('/search_user')
    @login_required
    def search_user():
        username = request.args.get('username', '').strip()
        
        if not username:
            return jsonify({'error': 'Please enter username'}), 400
            
        # Can't search for yourself
        if username == current_user.username:
            return jsonify({'error': 'Can\'t add yourself as a friend'}), 400
            
        # Query the user
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({'error': 'The user does not exist'}), 404
            
        # Check if you are already a friend
        is_friend = current_user.is_friends_with(user)
        
        # Return to user information
        return jsonify({
            'user': {
                'username': user.username,
                'avatar_color': user.avatar_color
            },
            'is_friend': is_friend
        })
    
    @application.route('/manage_ratings')
    @login_required
    def manage_ratings():
        """
        Show the table of all movies this user has rated,
        so they can update or delete each one.
        """
        user_movies = (
            UserMovie.query
            .join(Movie, Movie.id == UserMovie.movie_id)
            .filter(UserMovie.user_id == current_user.id)
            .all()
        )
        return render_template(
            'manage_ratings.html',
            user_movies=user_movies,
            underlined_tab_index=6  # if you’re using the same tab bar logic
        )
    
    @application.route('/manage_ratings/update/<int:user_movie_id>', methods=['POST'])
    @login_required
    def manage_ratings_update(user_movie_id):
        """
        Handle the form POST from the “Update” button.
        Expects `user_rating` in form-data.
        """
        new_rating = request.form.get('user_rating', type=float)
        if new_rating is None:
            flash("Please enter a valid rating.", "error")
            return redirect(url_for('manage_ratings'))

        link = UserMovie.query.filter_by(
            id=user_movie_id,
            user_id=current_user.id
        ).first()

        if not link:
            flash("Rating record not found.", "error")
            return redirect(url_for('manage_ratings'))

        link.user_rating = new_rating
        db.session.commit()
        flash(f"Rating for “{link.movie.title}” updated to {new_rating}.", "success")
        return redirect(url_for('manage_ratings'))


    @application.route('/manage_ratings/delete/<int:user_movie_id>', methods=['POST'])
    @login_required
    def manage_ratings_delete(user_movie_id):
        """
        Handle the form POST from the “Delete” button.
        """
        link = UserMovie.query.filter_by(
            id=user_movie_id,
            user_id=current_user.id
        ).first()

        if not link:
            flash("Rating record not found.", "error")
            return redirect(url_for('manage_ratings'))

        title = link.movie.title
        db.session.delete(link)
        db.session.commit()
        flash(f"Rating for “{title}” deleted.", "success")
        return redirect(url_for('manage_ratings'))

