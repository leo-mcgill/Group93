import os
import random
import json
from app import db
from app.models import User, Movie, UserMovie

def populate():
    """Populate DB with test data. Assumes active Flask app context."""
    file_path = os.path.join(os.path.dirname(__file__), 'example_movies.json')
    with open(file_path, 'r') as f:
        data = json.load(f)

    for movie in data:
        if not Movie.query.filter_by(title=movie['title']).first():
            db.session.add(Movie(
                title=movie['title'],
                year=movie['year'],
                rated=movie['rated'],
                released=movie['released'],
                runtime=movie['runtime'],
                genre=movie['genre'],
                director=movie['director'],
                writer=movie['writer'],
                actors=movie['actors'],
                language=movie['language'],
                country=movie['country'],
                imdb_rating=movie['imdb_rating'],
                rt_rating=movie['rt_rating'],
                metascore=movie['metascore'],
                box_office=movie['box_office'],
                poster_url=movie['poster_url']
            ))
    db.session.commit()

    user1 = User(username="user1")
    user1.set_password("password1")
    db.session.add(user1)

    user2 = User(username="user2")
    user2.set_password("password2")
    db.session.add(user2)

    user3 = User(username="user3")
    user3.set_password("password3")
    db.session.add(user3)

    db.session.commit()

    movie_titles = [
        "The Avengers", "The Lord of the Rings: The Return of the King", "How to Train Your Dragon",
        "The Super Mario Bros. Movie", "Hello, Dolly!", "Death Note",
        "Interstellar", "The Matrix", "Spirited Away"
    ]

    movies = {title: Movie.query.filter_by(title=title).first() for title in movie_titles}
    users = [user1, user2, user3]

    user_movies = [
        UserMovie(user_id=user1.id, movie_id=movies["The Avengers"].id, user_rating=random.uniform(1, 10)),
        UserMovie(user_id=user1.id, movie_id=movies["The Lord of the Rings: The Return of the King"].id, user_rating=random.uniform(1, 10)),
        UserMovie(user_id=user1.id, movie_id=movies["How to Train Your Dragon"].id, user_rating=random.uniform(1, 10)),

        UserMovie(user_id=user2.id, movie_id=movies["The Super Mario Bros. Movie"].id, user_rating=random.uniform(1, 10)),
        UserMovie(user_id=user2.id, movie_id=movies["Hello, Dolly!"].id, user_rating=random.uniform(1, 10)),
        UserMovie(user_id=user2.id, movie_id=movies["Death Note"].id, user_rating=random.uniform(1, 10)),

        UserMovie(user_id=user3.id, movie_id=movies["Interstellar"].id, user_rating=random.uniform(1, 10)),
        UserMovie(user_id=user3.id, movie_id=movies["The Matrix"].id, user_rating=random.uniform(1, 10)),
        UserMovie(user_id=user3.id, movie_id=movies["Spirited Away"].id, user_rating=random.uniform(1, 10)),
    ]
    db.session.add_all(user_movies)

    # Add friendships
    user1.friends.extend([user2, user3])
    user2.friends.extend([user1, user3])
    user3.friends.extend([user1, user2])

    db.session.commit()
    print("Test data populated successfully.")