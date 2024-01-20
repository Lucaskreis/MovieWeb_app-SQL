import csv
from .data_manager import DataManagerInterface

class CSVDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        with open(self.filename, "r") as file_obj:
            reader = csv.DictReader(file_obj)
            data = {row["id"]: row for row in reader}
            return data

    def get_user_movies(self, user_id):
        data = self.get_all_users()
        if user_id in data:
            return data[user_id]["name"], data[user_id]["movies"]
        else:
            return None, None

    def list_all_users(self):
        data = self.get_all_users()
        users_list = []

        for user_id, user_data in data.items():
            user_info = {
                "id": user_id,
                "name": user_data["name"]
            }
            users_list.append(user_info)

        return users_list

    def add_user(self, username):
        data = self.get_all_users()

        highest_id = max(map(int, data.keys()), default=0)
        new_user_id = str(highest_id + 1)
        while new_user_id in data:
            highest_id += 1
            new_user_id = str(highest_id)

        new_user = {
            "id": new_user_id,
            "name": username,
            "movies": ""
        }

        with open(self.filename, "a") as file_obj:
            writer = csv.DictWriter(file_obj, fieldnames=["id", "name", "movies"])
            writer.writerow(new_user)

    def add_movie_to_user(self, user_id, movie_data):
        data = self.get_all_users()

        if user_id in data:
            new_movie_id = self.generate_unique_id(data[user_id]["movies"])
            new_movie = {
                "id": new_movie_id,
                "title": movie_data["Title"],
                "poster": movie_data["Poster"],
                "rating": movie_data["imdbRating"],
                "year": movie_data["Year"]
            }
            data[user_id]["movies"] += f";{new_movie['id']}" if data[user_id]["movies"] else str(new_movie['id'])

            with open(self.filename, "w") as file_obj:
                writer = csv.DictWriter(file_obj, fieldnames=["id", "name", "movies"])
                writer.writeheader()
                writer.writerows(data.values())
        else:
            raise ValueError("User not found")


    def generate_unique_id(self, existing_movies):
        highest_id = max(map(lambda movie: int(movie), existing_movies.split(';')), default=0)
        new_id = highest_id + 1

        while str(new_id) in existing_movies:
            new_id += 1

        return str(new_id)

    def update_movie(self, user_id, movie_id, updated_movie):
        data = self.get_all_users()

        if user_id in data:
            movies = data[user_id]["movies"].split(';')
            for idx, movie in enumerate(movies):
                if movie == movie_id:
                    movies[idx] = updated_movie["id"]
                    movies_str = ';'.join(movies)
                    data[user_id]["movies"] = movies_str

                    with open(self.filename, "w") as file_obj:
                        writer = csv.DictWriter(file_obj, fieldnames=["id", "name", "movies"])
                        writer.writeheader()
                        writer.writerows(data.values())
                    break
            else:
                raise ValueError("Movie not found")
        else:
            raise ValueError("User not found")

    def delete_user(self, user_id):
        data = self.get_all_users()

        if user_id in data:
            del data[user_id]

            with open(self.filename, "w") as file_obj:
                writer = csv.DictWriter(file_obj, fieldnames=["id", "name", "movies"])
                writer.writeheader()
                writer.writerows(data.values())
        else:
            raise ValueError("User not found")

    def delete_movie(self, user_id, movie_id):
        data = self.get_all_users()

        if user_id in data:
            movies = data[user_id]["movies"].split(';')
            if movie_id in movies:
                movies.remove(movie_id)
                movies_str = ';'.join(movies)
                data[user_id]["movies"] = movies_str

                with open(self.filename, "w") as file_obj:
                    writer = csv.DictWriter(file_obj, fieldnames=["id", "name", "movies"])
                    writer.writeheader()
                    writer.writerows(data.values())
            else:
                raise ValueError("Movie not found")
        else:
            raise ValueError("User not found")