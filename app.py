from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Movie
import requests
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movieweb.db'
db.init_app(app)
URL = "http://www.omdbapi.com/?apikey=19391c77&"

# Home route
@app.route('/')
def home():
    return render_template('home.html')


# List all users route
@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)


# User movies route
@app.route('/users/<int:user_id>')
def user_movies(user_id):
    user = User.query.get(user_id)

    if user is None:
        return "User not found"

    movies = user.movies
    return render_template('user_movies.html', user=user, movies=movies)


# Add user route
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        new_user_name = request.form['username']
        new_user = User(username=new_user_name)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('list_users'))

    return render_template('add_user.html')


# Add movie route
@app.route('/add_movie/<int:user_id>', methods=['GET', 'POST'])
def add_movie(user_id):
    user = User.query.get(user_id)

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

        # Create a new Movie object using data from the API
        new_movie = Movie(
            user_id=user_id,
            title=movie_data.get('Title', ''),
            rating=movie_data.get('imdbRating', ''),
            year=movie_data.get('Year', ''),
            poster=movie_data.get('Poster', '')
        )

        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('add_movie.html', user=user)


# Update movie route
@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    user = User.query.get(user_id)

    if user is None:
        return "User not found"

    movie_to_update = Movie.query.get(movie_id)

    if movie_to_update is None or movie_to_update.user_id != user_id:
        return "Movie not found"

    if request.method == 'POST':
        movie_to_update.title = request.form['title']
        movie_to_update.rating = request.form['rating']
        movie_to_update.year = request.form['year']

        db.session.commit()
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('update_movie.html', user=user, movie=movie_to_update)


# Delete user route
@app.route('/users/<int:user_id>/delete_user')
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        # Delete associated movies first
        try:
            Movie.query.filter_by(user_id=user_id).delete()
            db.session.commit()
        except IntegrityError:
            db.session.rollback()  # Handle IntegrityError due to foreign key constraints

        # Now delete the user
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('list_users'))


# Delete movie route
@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    user = User.query.get(user_id)
    movie = Movie.query.get(movie_id)

    if user and movie and movie.user_id == user_id:
        db.session.delete(movie)
        db.session.commit()

    return redirect(url_for('user_movies', user_id=user_id))


# 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
