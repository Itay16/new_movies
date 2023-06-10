import requests
import storage_json
import random
import statistics
import json
import movies
from movies import movie_storage

API_KEY = '3863e126'
MOVIES_FILE = 'movie_storage.json'


def get_rating(movie):
    """Gets rating from a single movie"""
    return float(movie["rating"])


def _generate_website():
    with open(MOVIES_FILE, 'r') as newfile:
        all_movies = json.load(newfile)

    with open('index_template.html', 'r') as fileobj:
        html_template = fileobj.read()

    ADDRESS = f"http://www.omdbapi.com/?apikey={API_KEY}"
    movies_html = ""
    for movie in all_movies:
        movie_response = requests.get(f"{ADDRESS}&t={movie['title']}")
        movie_data = movie_response.json()
        poster = movie_data['Poster']
        year = movie_data['Year']
        title = movie_data['Title']
        movie_html = (
            '<li><br>'
            '<div class="movie">'
            f'<img class="movie-poster" src="{poster}"/><br>'
            f'<div class="movie-title">{title}</div><br>'
            f'<div class="movie-year">{year}</div><br>'
            '</div><br>'
            '</li><br>'
        )
        movies_html += movie_html
        html_output = html_template.replace('__TEMPLATE_TITLE__', "Itay's Movie Application")
        html_output = html_output.replace('__TEMPLATE_MOVIE_GRID__', movies_html)
    with open('index.html', 'w') as newfile:
        newfile.write(html_output)


class MovieApp:
    def __init__(self, storage):
        self.all_movies = None
        self._storage = storage

    def _command_list_movies(self):
        self.all_movies = self._storage.list_movies()

    def _command_movie_stats(self):
        """Gets all stats about the movies"""
        # average rating
        all_ratings = [float(movie['rating']) for movie in self.all_movies]
        average_rating = sum(all_ratings) / len(all_ratings)
        print(f"The average rating is: {average_rating}")

        # median rating
        median_rating = statistics.median(all_ratings)
        print(f"Median rating: {median_rating}")

        # best movie
        best_movies = []
        best_rating = max(all_ratings)
        for movie in self.all_movies:
            if float(movie['rating']) == best_rating:
                best_movies.append(movie['title'])
        if len(best_movies) > 1:
            print("The best movies are:")
            for movie in best_movies:
                print(f"{movie}: {best_rating}")
        else:
            print(f"The best rated movie is: {best_movies[0]}, {best_rating}!")

        # worst movie
        worst_movies = []
        worst_rating = min(all_ratings)
        for movie in self.all_movies:
            if float(movie['rating']) == worst_rating:
                worst_movies.append(movie['title'])
        if len(worst_movies) > 1:
            print("The worst rated movies are:")
            for movie in worst_movies:
                print(f"{movie}: {worst_rating}")
        else:
            print(f"The worst movie is: {worst_movies[0]}, {worst_rating}!")


def run():
    """Main function"""
    with open(MOVIES_FILE, 'r') as newfile:
        all_movies = json.load(newfile)
    print("***Welcome to - My Movies Database!***")
    movies.menu()
    user_choice = input("Enter a number (0-9): ")
    while user_choice != '0':
        if user_choice == '1':
            movie_storage.list_movies(MOVIES_FILE)
        elif user_choice == '2':
            movie_storage.add_movie(all_movies, API_KEY)
        elif user_choice == '3':
            movie_storage.delete_movie(MOVIES_FILE)
        elif user_choice == '4':
            movie_storage.update_movie(all_movies)
        elif user_choice == '5':
            MovieApp._command_movie_stats(all_movies)
        elif user_choice == '6':
            all_movies.random_movie(all_movies)
        elif user_choice == '7':
            all_movies.search_for_movie(all_movies)
        elif user_choice == '8':
            all_movies.sort_movies_by_rating(all_movies)
        elif user_choice == '9':
            _generate_website()
            print("Website generated successfully!")
        else:
            print("\nInvalid choice!\n")
        movies.menu()
        user_choice = input("Enter a number (0-9): ")
    print("Goodbye!")


if __name__ == "__main__":
    run()
