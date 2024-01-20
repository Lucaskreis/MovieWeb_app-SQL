from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Movie
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movieweb.db'
db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def user_movies(user_id):
    user, movies = data_manager.get_user_movies(user_id)

    if user is None:
        return "User not found"

    return render_template('user_movies.html', user_id=user_id, user=user, movies=movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        new_user_name = request.form['username']
        data_manager.add_user(new_user_name)
        return redirect(url_for('list_users'))
    return render_template('add_user.html')


@app.route('/add_movie/<user_id>', methods=['GET', 'POST'])
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

    return render_template('add_movie.html', user=user)


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    user, movies = data_manager.get_user_movies(user_id)

    if user is None:
        return "User not found"

    movie_to_update = next((movie for movie in movies if movie["id"] == int(movie_id)), None)

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


@app.route('/users/<user_id>/delete_user')
def delete_user(user_id):
    try:
        data_manager.delete_user(user_id)
        return redirect(url_for('list_users'))
    except ValueError as e:
        return f"Error: {str(e)}"


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(user_id, movie_id):
    user, _ = data_manager.get_user_movies(user_id)

    if user is None:
        return "User not found"

    data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    # Create the database tables based on the defined models
    db.create_all()
    app.run(debug=True)




