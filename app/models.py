from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    movies = db.relationship('Movie', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    year = db.Column(db.String(4), nullable=True)  # e.g., "1999"
    rated = db.Column(db.String(10), nullable=True)  # e.g., "R"
    released = db.Column(db.String(20), nullable=True)  # e.g., "31 Mar 1999"
    runtime = db.Column(db.Integer, nullable=False)  # In minutes, e.g., 136
    genre = db.Column(db.String(100), nullable=True)  # e.g., "Action, Sci-Fi"
    director = db.Column(db.String(200), nullable=True)  # e.g., "Lana Wachowski, Lilly Wachowski"
    writer = db.Column(db.String(200), nullable=True)  # e.g., "Lana Wachowski, Lilly Wachowski"
    actors = db.Column(db.String(200), nullable=False)  # e.g., "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss"
    language = db.Column(db.String(100), nullable=True)  # e.g., "English"
    country = db.Column(db.String(100), nullable=True)  # e.g., "United States"
    user_rating = db.Column(db.Float, nullable=True)  # User’s rating (0-10)
    imdb_rating = db.Column(db.Float, nullable=True)  # e.g., 8.7
    rt_rating = db.Column(db.String(10), nullable=True)  # e.g., "88%"
    metascore = db.Column(db.Integer, nullable=True)  # e.g., 73
    box_office = db.Column(db.String(20), nullable=True)  # e.g., "$171,479,930"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)