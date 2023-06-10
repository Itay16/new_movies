from abc import ABC, abstractmethod
import requests
import json
import movies
import storage_json
import storage_csv
import random
from movies import Movie

API_KEY = '3863e126'
MOVIES_FILE = 'movie_storage.json'


class MovieApp:
    def __init__(self, storage):
        self._storage = storage
        self.all_movies = self._storage.list_movies()

    def list_movies(self):
        self.all_movies = self._storage.list_movies()
        if not self.all_movies:
            print("No movies found.")
        else:
            for i in range(len(self.all_movies)):
                movie_data = self.all_movies[i]
                movie = Movie(movie_data['title'], movie_data['year'], movie_data['rating'])
                print(f"{i + 1}. {movie.title} ({movie.year}): {movie.rating}")

    def add_movie(self):
        """Add a movie to the database"""
        title = input("Enter the movie title: ")

        try:
            # Make a request to the movies API to fetch movie details
            response = requests.get(f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}")
            response.raise_for_status()  # Raise an exception if the request was unsuccessful
            movie_data = response.json()

            if movie_data.get('Response') == 'True':
                movie = {
                    'title': movie_data['Title'],
                    'year': movie_data['Year'],
                    'rating': movie_data['imdbRating'],
                }

                movies = self._storage.list_movies()  # Read existing movies from storage
                movies.append(movie)  # Add the new movie
                self._storage.write_movies(movies)  # Write all movies back to storage

                print(f"Movie '{movie['title']} ({movie['year']})' added successfully.")
            else:
                print("Movie not found.")
        except ConnectionError:
            print("Sorry, it seems like you're not connected to the internet!")

    def search_for_movie(self):
        """Searches the database for a movie based on a string"""
        user_search = input("\nEnter the movie's name: ").lower()
        found_movies = [movie for movie in self.all_movies if user_search in movie['title'].lower()]
        if found_movies:
            print("I found:")
            for movie in found_movies:
                print(f"{movie['title']} ({movie['year']})")
        else:
            print("No movies found.")

    def random_movie(self):
        """Generates a random movie"""
        if self.all_movies:
            movie_random = random.choice(self.all_movies)
            print(f"{movie_random['title']} ({movie_random['year']}): {movie_random['rating']}")
        else:
            print("No movies found.")

    def get_rating(self, movie):
        """Gets rating from a single movie"""
        return float(movie["rating"])

    import requests

    def generate_website(self):
        if self.all_movies:
            with open('index_template.html', 'r') as fileobj:
                html_template = fileobj.read()

            movies_html = ""
            ADDRESS = f"http://www.omdbapi.com/?apikey={API_KEY}"
            for movie in self.all_movies:
                movie_title = movie['title']
                movie_response = requests.get(f"{ADDRESS}&t={movie_title}")
                movie_data = movie_response.json()

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

            with open('index.html', 'w') as newfile:
                newfile.write(html_output)

            print("Website generated successfully!")
        else:
            print("No movies found.")

    def sort_movies_by_rating(self):
        """Sorts movies from best to worst"""
        if self.all_movies:
            sorted_movies = sorted(self.all_movies, key=self.get_rating, reverse=True)
            for movie in sorted_movies:
                print(f"{movie['title']} ({movie['year']}): {movie['rating']}")
        else:
            print("No movies found.")

    def movie_stats(self):
        """Display statistics about the movies"""
        all_movies = self._storage.list_movies()  # Get the movies from storage

        total_movies = len(all_movies)
        ratings = [float(movie['rating']) for movie in all_movies]

        highest_rating = max(ratings)
        lowest_rating = min(ratings)
        average_rating = sum(ratings) / total_movies

        print("\nMovie Statistics:")
        print(f"Highest rating: {highest_rating}")
        print(f"Lowest rating: {lowest_rating}")
        print(f"Average rating: {average_rating:.2f}")
        print()

    def run(self):
        """Main function"""
        print("***Welcome to - My Movies Database!***")
        movies.menu()
        user_choice = input("Enter a number (0-9): ")

        while user_choice != '0':
            if user_choice == '1':
                self.list_movies()
            elif user_choice == '2':
                self._storage.add_movie()
                self.all_movies = self._storage.list_movies()
            elif user_choice == '3':
                title_to_delete = input("Enter the title of the movie you want to delete: ")
                self._storage.delete_movie(title_to_delete)
                self.all_movies = self._storage.list_movies()
            elif user_choice == '4':
                title_to_update = input("Enter the title of the movie you want to update: ")
                new_rating = input("Enter the new rating: ")
                self._storage.update_movie(title_to_update, new_rating)
                self.all_movies = self._storage.list_movies()
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
