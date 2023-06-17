import json


def menu():
    """Menu of all available commands"""
    print("""Menu:
0. Exit
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Generate website
""")


class Movie:
    def __init__(self, title, year, rating):
        self.title = title
        self.year = year
        self.rating = rating


class JsonStorage:
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        with open(self.file_path, 'r') as file:
            movies_data = json.load(file)
        return movies_data

    def add_movie(self, movie):
        movies_data = self.list_movies()
        movies_data.append(movie)
        with open(self.file_path, 'w') as file:
            json.dump(movies_data, file)

    def delete_movie(self, title):
        movies_data = self.list_movies()
        movies_data = [movie for movie in movies_data if movie['title'].lower() != title.lower()]
        with open(self.file_path, 'w') as file:
            json.dump(movies_data, file)

    def update_movie(self, title, new_rating):
        movies_data = self.list_movies()
        for movie in movies_data:
            if movie['title'].lower() == title.lower():
                movie['rating'] = new_rating
                break
        with open(self.file_path, 'w') as file:
            json.dump(movies_data, file)
