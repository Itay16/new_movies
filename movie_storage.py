import json
import requests

API_KEY = '3863e126'
MOVIES_FILE = 'movie_storage.json'

with open(MOVIES_FILE, 'r') as newfile:
    movies = json.load(newfile)


def list_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data. 

    For example, the function may return:
    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      },
      "..." {
        ...
      },
    }
    """
    print(f"\n{len(movies)} movies in total:")
    for movie in movies:
        rating = movie['rating']
        title = movie['title']
        year = movie['year']
        print(f"{title} ({year}): {rating}")
    print('\n')


def add_movie():
    """
      Adds a movie to the movies' database.
      Loads the information from the JSON file, add the movie,
      and saves it. The function doesn't need to validate the input.
    """
    new_movie_title = input("Enter the name of the new movie: ")
    ADDRESS = f"http://www.omdbapi.com/?apikey={API_KEY}"
    movie_response = requests.get(f"{ADDRESS}&t={new_movie_title}")
    new_data = movie_response.json()
    try:
        for info in new_data:
            title = new_data['Title']
            year = new_data['Year']
            new_rating = float(new_data['imdbRating'])
        new_movie = {
            'title': new_movie_title,
            'rating': new_rating,
            'year': year
        }
        # Add the new movie to the list of movies
        movies.append(new_movie)
        # Write the updated data back to the file
        with open("movie_storage.json", "w") as f:
            json.dump(movies, f)
        print(f"Added {new_movie_title} ({year}) with rating {new_rating} to database!")
    except KeyError:
        print("That movie doesn't exist!")
    except ConnectionError:
        print("Hmm... It doesn't look like you have internet!")


def delete_movie(movies_file):
    """
    Deletes a movie from the movies' database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    title_to_delete = input("Enter the title of the movie you want to delete: ")
    with open(movies_file, 'r') as new_file:
        movies = json.load(new_file)
    for movie in movies:
        if movie['title'] == title_to_delete:
            movies.remove(movie)
            with open(movies_file, 'w') as f:
                json.dump(movies, f)
            print(f"{movie['title']} was removed from the database.")
            return
        print(f"{title_to_delete} was not found in the database.")


def update_movie(movies):
    """
    Updates a movie from the movies' database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    title_to_update = input("Enter the title of the movie you want to update: ")
    for movie in movies:
        if movie['title'] == title_to_update:
            movie['title'] = input("Enter the new title: ")
            movie['year'] = input("Enter the new year: ")
            movie['rating'] = input("Enter the new rating: ")
            print(f"{title_to_update} was updated.")
        return
    print(f"{title_to_update} was not found in the database.")
