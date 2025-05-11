from models import *
from sqlalchemy.orm import aliased

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

def query_for_movies_rated(current_user):
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

    #movies = query.all()
    return query

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

def get_movies_of_genre(all_movies, max_genre):
    movies_of_genre = []
    for movie in all_movies:
        genre_string = movie.genre
        genres = [genre.strip() for genre in genre_string.split(",")]
        if max_genre in genres:
            movies_of_genre.append((movie))
            
    return movies_of_genre

def get_friend_movies(friend_username):
    # Return False if no friend is selected
    if friend_username == None:
        return False

    friend = User.query.filter_by(username=friend_username).first()

    user_movie_alias = aliased(UserMovie)

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
