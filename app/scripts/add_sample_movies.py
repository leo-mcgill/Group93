#Group 93 CITS3403 Project 2025
#script to add sample movies from example_movies.json

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import create_app, db
from app.models import User, Movie

import json

application = create_app()

with application.app_context():

    with open('app/scripts/example_movies.json', 'r') as f:
        data = json.load(f)

    for movie in data:
        existing = Movie.query.filter_by(title=movie['title']).first()
        if existing:
            continue
        movie = Movie(
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
                )
        db.session.add(movie)
    db.session.commit()
    
    print("Test data added.")
