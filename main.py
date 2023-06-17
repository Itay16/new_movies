from movie_app import MovieApp
from data import storage_json

API_KEY = '3863e126'
MOVIES_FILE = 'data/movie_storage.json'


def main():
    """Main function"""
    storage = storage_json.JsonStorage(MOVIES_FILE)
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
