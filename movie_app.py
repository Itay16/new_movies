import os
import random

import requests

import movies
from movies import Movie

API_KEY = '3863e126'
MOVIES_FILE = 'data/movie_storage.json'
ADDRESS = f'http://www.omdbapi.com/?apikey={API_KEY}'
OUTPUT_FOLDER = 'output_folder'
CSS_FILE = 'static/style.css'


class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def list_movies(self):
        all_movies = self._storage.list_movies()
        if not all_movies:
            print("No movies found.")
        else:
            for i, movie_data in enumerate(all_movies, start=1):
                movie = Movie(movie_data['title'], movie_data['year'], movie_data['rating'])
                print(f"{i}. {movie.title} ({movie.year}): {movie.rating}")

    def add_movie(self):
        """Add a movie to the database"""
        title = input("Enter the movie title: ")

        try:
            movie_data = self.fetch_movie_data(title)

            if movie_data.get('Response') == 'True':
                movie = {
                    'title': movie_data['Title'],
                    'year': movie_data['Year'],
                    'rating': movie_data['imdbRating'],
                }

                self._storage.add_movie(movie)  # Pass the movie to add_movie method
                print(f"Movie '{movie['title']} ({movie['year']})' added successfully.")
            else:
                print("Movie not found.")
        except ConnectionError:
            print("Sorry, it seems like you're not connected to the internet!")

    def fetch_movie_data(self, title):
        """Fetches movie details from the OMDB API"""
        response = requests.get(f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}")
        response.raise_for_status()
        return response.json()

    def search_for_movie(self):
        """Searches the database for a movie based on a string"""
        user_search = input("\nEnter the movie's name: ").lower()
        found_movies = [movie for movie in self._storage.list_movies() if user_search in movie['title'].lower()]
        if found_movies:
            print("I found:")
            for movie in found_movies:
                print(f"{movie['title']} ({movie['year']})")
        else:
            print("No movies found.")

    def random_movie(self):
        """Generates a random movie"""
        all_movies = self._storage.list_movies()
        if all_movies:
            movie_random = random.choice(all_movies)
            print(f"{movie_random['title']} ({movie_random['year']}): {movie_random['rating']}")
        else:
            print("No movies found.")

    def get_rating(self, movie):
        """Gets rating from a single movie"""
        return float(movie["rating"])

    def generate_website(self):
        all_movies = self._storage.list_movies()
        if all_movies:
            with open('templates/index_template.html', 'r') as fileobj:
                html_template = fileobj.read()

            movies_html = ""
            for movie in all_movies:
                movie_title = movie['title']
                movie_data = self.fetch_movie_data(movie_title)

                if movie_data['Response'] == 'True':
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

            css_code = ""
            css_file_path = os.path.join('static', 'style.css')
            with open(css_file_path, 'r') as css_file:
                css_code = css_file.read()

            html_output = html_output.replace('__TEMPLATE_CSS__', css_code)

            with open('templates/index.html', 'w') as newfile:
                newfile.write(html_output)

            print("Website generated successfully!")
        else:
            print("No movies found.")

    def sort_movies_by_rating(self):
        """Sorts movies from best to worst"""
        all_movies = self._storage.list_movies()
        if all_movies:
            sorted_movies = sorted(all_movies, key=self.get_rating, reverse=True)
            for movie in sorted_movies:
                print(f"{movie['title']} ({movie['year']}): {movie['rating']}")
        else:
            print("No movies found.")

    def movie_stats(self):
        """Display statistics about the movies"""
        all_movies = self._storage.list_movies()
        if all_movies:
            ratings = [float(movie['rating']) for movie in all_movies]

            highest_rating = max(ratings)
            lowest_rating = min(ratings)
            average_rating = sum(ratings) / len(all_movies)

            print("\nMovie Statistics:")
            print(f"Highest rating: {highest_rating}")
            print(f"Lowest rating: {lowest_rating}")

            highest_rated_movies = [movie for movie in all_movies if float(movie['rating']) == highest_rating]
            print("Movies with the highest rating:")
            for movie in highest_rated_movies:
                print(f"{movie['title']} ({movie['year']}): {movie['rating']}")

            lowest_rated_movies = [movie for movie in all_movies if float(movie['rating']) == lowest_rating]
            print("Movies with the lowest rating:")
            for movie in lowest_rated_movies:
                print(f"{movie['title']} ({movie['year']}): {movie['rating']}")

            print(f"Average rating: {average_rating:.2f}")
            print()
        else:
            print("No movies found.")

    def run(self):
        """Main function"""
        print("***Welcome to - My Movies Database!***")
        movies.menu()
        user_choice = input("Enter a number (0-9): ")

        while user_choice != '0':
            if user_choice == '1':
                self.list_movies()
            elif user_choice == '2':
                self.add_movie()
            elif user_choice == '3':
                title_to_delete = input("Enter the title of the movie you want to delete: ")
                self._storage.delete_movie(title_to_delete)
            elif user_choice == '4':
                title_to_update = input("Enter the title of the movie you want to update: ")
                new_rating = input("Enter the new rating: ")
                self._storage.update_movie(title_to_update, new_rating)
            elif user_choice == '5':
                self.movie_stats()
            elif user_choice == '6':
                self.random_movie()
            elif user_choice == '7':
                self.search_for_movie()
            elif user_choice == '8':
                self.sort_movies_by_rating()
            elif user_choice == '9':
                self.generate_website()
            else:
                print("\nInvalid choice!\n")

            movies.menu()
            user_choice = input("Enter a number (0-9): ")

        print("Goodbye!")


if __name__ == "__main__":
    storage = movies.Movie(MOVIES_FILE)
    app = MovieApp(storage)
    app.run()
