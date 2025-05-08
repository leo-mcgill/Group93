from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

user_friends = db.Table('user_friends',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', name='fk_user_friends_user_id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id', name='fk_user_friends_friend_id'), primary_key=True)
)

class UserMovie(db.Model):
    __tablename__ = 'user_movie'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_user_movie_user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id', name='fk_user_movie_movie_id'), nullable=False)
    user_rating = db.Column(db.Float, nullable=True)

    # Unique constraint to prevent duplicate (user, movie) entries
    __table_args__ = (db.UniqueConstraint('user_id', 'movie_id', name='_user_movie_uc'),)

    # Relationships
    user = db.relationship("User", back_populates="user_movies")
    movie = db.relationship("Movie", back_populates="user_movies")
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    user_movies = db.relationship("UserMovie", back_populates="user", cascade="all, delete-orphan")

    def movies(self):
        return [um.movie for um in self.user_movies]

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    friends = db.relationship('User', 
                              secondary=user_friends, 
                              primaryjoin=(user_friends.c.user_id == id), 
                              secondaryjoin=(user_friends.c.friend_id == id),
                              backref=db.backref('friends_of', lazy='dynamic'))
    
    def is_friends_with(self, other_user):
        return other_user in self.friends
    

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    year = db.Column(db.String(4), nullable=True)
    rated = db.Column(db.String(10), nullable=True)
    released = db.Column(db.String(20), nullable=True)
    runtime = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100), nullable=True)
    director = db.Column(db.String(200), nullable=True)
    writer = db.Column(db.String(200), nullable=True)
    actors = db.Column(db.String(200), nullable=False)
    language = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    imdb_rating = db.Column(db.Float, nullable=True)
    rt_rating = db.Column(db.String(10), nullable=True)
    metascore = db.Column(db.Integer, nullable=True)
    box_office = db.Column(db.String(20), nullable=True)
    poster_url = db.Column(db.String(200), nullable=True)

    user_movies = db.relationship("UserMovie", back_populates="movie", cascade="all, delete-orphan")
    
