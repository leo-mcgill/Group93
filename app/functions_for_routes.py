#Group 93 CITS3403 Project 2025
#functions used by routes. These functions are imported by routes.py

from app.models import *
from sqlalchemy.orm import aliased

from collections import Counter

# packs the movie_list into a json. This excludes user ratings.
def pack_movie_data_list(movies):
    movies_data = []
    for movie in movies:
        movies_data.append({
            "title": movie.title,
            "year": movie.year,
            "rated": movie.rated,
            "released": movie.released,
            "genre": movie.genre,
            "director": movie.director,
            "writer": movie.writer,
            "actors": movie.actors,
            "imdb_rating": movie.imdb_rating,
            "metascore": movie.metascore,
            "box_office": movie.box_office,
            "poster_url": movie.poster_url,
        })
    return movies_data

# Get the highest user-rated movie
def get_favorite_movies(user_id, limit=6):
    # Get the highest user-rated movie
    favorite_movies = UserMovie.query.filter_by(user_id=user_id)\
        .filter(UserMovie.user_rating.isnot(None))\
        .order_by(UserMovie.user_rating.desc(),UserMovie.id.desc())\
        .limit(limit)\
        .all()
    
    return favorite_movies

# Obtain user's movie viewing statistics
def get_movie_stats(user_id):
    # Get all rated movies from users
    user_movies = UserMovie.query.filter_by(user_id=user_id)\
        .filter(UserMovie.user_rating.isnot(None)).all()
    
    # Total rated movies
    total_movies = len(user_movies)
    
    if total_movies == 0:
        return {
            "total_movies": 0,
            "avg_rating": 0,
            "favorite_genres": [],
            "ratings_distribution": {},
            "highest_rated": None
        }
    
    # Calculate the average score
    avg_rating = sum(um.user_rating for um in user_movies) / total_movies
    
    # Get all movie types and count
    genres = []
    for um in user_movies:
        if um.movie.genre:
            for genre in um.movie.genre.split(','):
                genres.append(genre.strip())
    
    # Calculate the most frequently viewed types
    genre_counter = Counter(genres)
    top_genres = genre_counter.most_common(3)
    
    # Calculate the scoring distribution
    ratings_distribution = {}
    for um in user_movies:
        # Round to the nearest integer
        rating_int = round(um.user_rating)
        ratings_distribution[rating_int] = ratings_distribution.get(rating_int, 0) + 1
    
    # Find the highest rated movie
    highest_rated = None
    if user_movies:
        highest_rated = max(user_movies, key=lambda um: um.user_rating)
    
    return {
        "total_movies": total_movies,
        "avg_rating": round(avg_rating, 1),
        "favorite_genres": top_genres,
        "ratings_distribution": ratings_distribution,
        "highest_rated": highest_rated
    }

# packs the movie data into a json. This includes user ratings.
def pack_movie_data_tuple(movies):
    movies_data = []
    for movie, user_rating in movies:
        movies_data.append({
            "title": movie.title,
            "year": movie.year,
            "rated": movie.rated,
            "released": movie.released,
            "genre": movie.genre,
            "director": movie.director,
            "writer": movie.writer,
            "actors": movie.actors,
            "imdb_rating": movie.imdb_rating,
            "metascore": movie.metascore,
            "box_office": movie.box_office,
            "poster_url": movie.poster_url,
            "user_rating": user_rating
        })
    return movies_data

# creates and returns a query for the movies that have been rated of a user.
def query_for_movies_rated(current_user):
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

    return query

# Uses a simple sum of ratings of all movies of genres, then returns the max genre of a a user's movies
def calculate_top_genre(movies):
    movie_genre_ratings = {}

    for movie, user_rating in movies:
        genre_string = movie.genre
        genres = [genre.strip() for genre in genre_string.split(",")]
        for genre in genres:
            if genre in movie_genre_ratings:
                movie_genre_ratings[genre] += user_rating
            else:
                movie_genre_ratings[genre] = user_rating

    if len(movie_genre_ratings) == 0:
        return "NULL"
    top_genre = max(movie_genre_ratings, key=movie_genre_ratings.get)

    return top_genre

# Looks through list of all movies and takes out all the movies which belong to a specific genre.
def get_movies_of_genre(all_movies, max_genre):
    movies_of_genre = []
    for movie in all_movies:
        genre_string = movie.genre
        genres = [genre.strip() for genre in genre_string.split(",")]
        if max_genre in genres:
            movies_of_genre.append((movie))
            
    return movies_of_genre

# Queries for all the movies that a friend has rated and returns the list of tuples of movie, and friend_ratings.
def get_friend_movies(current_user, friend_username):
    # Return False if no friend is selected
    if friend_username == None:
        return False

    friend = User.query.filter_by(username=friend_username).first()

    user_movie_alias = aliased(UserMovie)

    users_shared = current_user.friends

    users_shared_usernames = []
    for user in users_shared:
        users_shared_usernames.append(user.username)

    #checks if friend_username actually exists in the current user's friend usernames
    if friend.username not in users_shared_usernames:
        print("friend_username field was not present in the current user's friends")
        return None

    query = (
        db.session.query(
            Movie,
            user_movie_alias.user_rating
        )
        .outerjoin(
            user_movie_alias,
            (Movie.id == user_movie_alias.movie_id) & (user_movie_alias.user_id == friend.id)
        )
        .filter(user_movie_alias.user_rating.isnot(None))  # Only movies the friend has rated
    )

    movies = query.all()
    return movies

