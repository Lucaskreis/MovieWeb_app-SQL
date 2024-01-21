from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    movies = db.relationship('Movie', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)


class Movie(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.DECIMAL(3, 1))
    year = db.Column(db.Integer)
    poster = db.Column(db.String(255))
    reviews = db.relationship('Review', backref='movie', lazy=True)


class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), nullable=False)
    text_review = db.Column(db.Text, nullable=False)
    date_review = db.Column(db.DateTime, default=datetime.utcnow)
    #username = db.Column(db.String(255), nullable=False)