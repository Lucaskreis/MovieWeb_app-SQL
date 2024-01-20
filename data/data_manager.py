from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def list_all_users(self):
        pass

    @abstractmethod
    def add_user(self, username):
        pass

    @abstractmethod
    def add_movie_to_user(self, user_id, movie_data):
        pass

    @abstractmethod
    def generate_unique_id(self, existing_movies):
        pass

    @abstractmethod
    def update_movie(self, user_id, movie_id, updated_movie):
        pass

    @abstractmethod
    def delete_user(self, user_id):
        pass

    @abstractmethod
    def delete_movie(self, user_id, movie_id):
        pass
