from models import db, User, Movie, Review
from data.data_manager import DataManagerInterface
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movieweb.db'
        self.db = SQLAlchemy(self.app)

    def add_user(self, username):
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()

    def list_all_users(self):
        return User.query.all()

    def get_user_movies(self, user_id):
        user = User.query.get(user_id)
        if user:
            movies = user.movies
            return user, movies
        return None, None

    def add_movie_to_user(self, user_id, movie_data):
        user = User.query.get(user_id)
        if user:
            new_movie = Movie(
                user_id=user_id,
                title=movie_data.get('Title'),
                rating=movie_data.get('imdbRating'),
                year=movie_data.get('Year'),
                poster=movie_data.get('Poster')
            )
            db.session.add(new_movie)
            db.session.commit()

    def update_movie(self, user_id, movie_id, updated_movie_data):
        movie = Movie.query.get(movie_id)
        if movie and movie.user_id == user_id:
            movie.title = updated_movie_data.get('title')
            movie.rating = updated_movie_data.get('rating')
            movie.year = updated_movie_data.get('year')
            movie.poster = updated_movie_data.get('Poster')
            db.session.commit()

    def delete_user(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

    def delete_movie(self, user_id, movie_id):
        movie = Movie.query.get(movie_id)
        if movie and movie.user_id == user_id:
            db.session.delete(movie)
            db.session.commit()

    def get_movie_by_id(self, movie_id):
        return Movie.query.get(movie_id)

    def add_review_to_movie(self, movie_id, username, review_text, review_date):
        movie = self.get_movie_by_id(movie_id)

        if movie:
            review = Review(username=username, text=review_text, date=review_date)
            movie.reviews.append(review)

            db.session.add(movie)
            db.session.commit()

    def delete_review(self, review_id):
        review = Review.query.get(review_id)
        if review:
            db.session.delete(review)
            db.session.commit()