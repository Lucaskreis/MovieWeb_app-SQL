from models import db, User, Movie


class SQLiteDataManager:
    def __init__(self):
        pass  # Optionally, you can initialize any required configurations here

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
                year=movie_data.get('Year')
            )
            db.session.add(new_movie)
            db.session.commit()

    def update_movie(self, user_id, movie_id, updated_movie_data):
        movie = Movie.query.get(movie_id)
        if movie and movie.user_id == user_id:
            movie.title = updated_movie_data.get('title')
            movie.rating = updated_movie_data.get('rating')
            movie.year = updated_movie_data.get('year')
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
