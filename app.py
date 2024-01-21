from data.SQLiteDataManager import SQLiteDataManager
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Movie, Review
import requests
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.secret_key = 'masterschool'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movieweb.db'
db.init_app(app)

data_manager = SQLiteDataManager('instance/movieweb.db')


# Home route
@app.route('/')
def home():
    return render_template('home.html')


# List all users route
@app.route('/users')
def list_users():
    users = data_manager.list_all_users()
    return render_template('users.html', users=users)


# User movies route
@app.route('/users/<int:user_id>')
def user_movies(user_id):
    user, movies = data_manager.get_user_movies(user_id)

    if user is None:
        return "User not found"

    return render_template('user_movies.html', user=user, movies=movies)


# Add user route
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        new_user_name = request.form['username']
        data_manager.add_user(new_user_name)
        return redirect(url_for('list_users'))
    return render_template('add_user.html')


# Add movie route
@app.route('/add_movie/<int:user_id>', methods=['GET', 'POST'])
def add_movie(user_id):
    user, _ = data_manager.get_user_movies(user_id)
    if user is None:
        return "User not found"

    if request.method == 'POST':
        movie_title = request.form['movie_title']
        # Fetch movie data from OMDB API
        omdb_api_key = "19391c77"
        omdb_api_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={movie_title}"
        response = requests.get(omdb_api_url)
        movie_data = response.json()

        if "Error" in movie_data:
            return f"Error: {movie_data['Error']}"

        data_manager.add_movie_to_user(user_id, movie_data)
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('user_movies.html', user=user, movies=_, user_id=user_id)


# Update movie route
@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    user, movies = data_manager.get_user_movies(user_id)

    if user is None:
        return "User not found"

    movie_to_update = None
    for movie in movies:
        if movie.movie_id == movie_id:
            movie_to_update = movie
            break

    if movie_to_update is None:
        return "Movie not found"

    if request.method == 'POST':
        updated_movie = {
            "title": request.form['title'],
            "rating": request.form['rating'],
            "year": request.form['year']
        }
        data_manager.update_movie(user_id, movie_id, updated_movie)
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('update_movie.html', user=user, movie=movie_to_update)


# Delete user route
@app.route('/users/<int:user_id>/delete_user')
def delete_user(user_id):
    try:
        data_manager.delete_user(user_id)
        return redirect(url_for('list_users'))
    except ValueError as e:
        return f"Error: {str(e)}"


# Delete movie route
@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    user, _ = data_manager.get_user_movies(user_id)

    if user is None:
        return "User not found"

    data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/movies')
def list_movies():
    movies = Movie.query.all()
    return render_template('movies.html', movies=movies)


@app.route('/movies/<int:movie_id>')
def movie_review(movie_id):
    movie = data_manager.get_movie_by_id(movie_id)
    if movie is None:
        return "User not found"
    reviews = movie.reviews
    return render_template('movie_review.html', movie=movie, reviews=reviews)


@app.route('/movies/<int:movie_id>/add_review', methods=['GET', 'POST'])
def add_review(movie_id):
    movie_to_review = data_manager.get_movie_by_id(movie_id)

    if movie_to_review is None:
        return "Movie not found"

    if request.method == 'POST':
        username = request.form['username']
        review_text = request.form['review_text']
        review_date = datetime.now()

        data_manager.add_review_to_movie(movie_id, username, review_text, review_date)

        flash('Review added successfully!', 'success')
        return redirect(url_for('movie_review', movie_id=movie_id))

    return render_template('add_review.html', movie=movie_to_review)


@app.route('/movie/<int:movie_id>/add_review/<int:review_id>')
def delete_review(movie_id, review_id):
    data_manager.delete_review(review_id)
    return redirect(url_for('list_movies'))


# 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
