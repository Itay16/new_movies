from movie_app import MovieApp
from storage_json import JsonStorage


API_KEY = '3863e126'
MOVIES_FILE = 'movie_storage.json'


def main():
    """Main function"""
    storage = JsonStorage(MOVIES_FILE)
    movie_app = MovieApp(storage)
    movie_app.run()

if __name__ == "__main__":
    main()
