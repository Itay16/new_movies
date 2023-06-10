import statistics
import random

API_KEY = '3863e126'
MOVIES_FILE = 'movie_storage.json'


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


def stats(movies):
    """Gets all stats about the movies"""
    # average rating
    all_ratings = [float(movie['rating']) for movie in movies]
    average_rating = sum(all_ratings) // len(all_ratings)
    print(f"The average rating is: {average_rating}")

    # median rating
    median_rating = statistics.median(all_ratings)
    print(f"Median rating: {median_rating}")

    # best movie
    best_movies = []
    best_rating = max(all_ratings)
    for movie in movies:
        if movie['rating'] == best_rating:
            best_movies.append(movie['title'])
    if len(best_movies) > 1:
        print("The best movies are: ")
        for movie in best_movies:
            print(f"{movie['title']}: {best_rating}")
    else:
        print(f"The best rated movie is: {best_movies[0]}, {best_rating}!")

    # worst movie
    worst_movies = []
    worst_rating = min(all_ratings)
    for movie in movies:
        if movie['rating'] == worst_rating:
            worst_movies.append(movie['title'])
    if len(worst_movies) > 1:
        print("The worst rated movies are: ")
        for movie in worst_movies:
            print(f"{movie['title']}: {worst_rating}")
    else:
        print(f"The worst movie is: {worst_movies[0]}, {worst_rating}!")


def random_movie(movies):
    """Generates a random movie"""
    movie_random = random.choice(movies)
    print(f"{movie_random['title']} ({movie_random['year']}): {movie_random['rating']}")


def search_for_movie(movies):
    """Searches database for a movie based on a string"""
    user_search = input("\nEnter the movie's name: ")
    user_search = user_search.lower()
    for movie in movies:
        if user_search in movie['title'].lower():
            print(f"I found: \n{movie['title']} ({movie['year']})\n")


def get_rating(movie):
    """Gets rating from a single movie"""
    return float(movie['rating'])


def sort_movies_by_rating(movies):
    """Sorts movies from best to worst"""
    sorted_movies = sorted(movies, key=get_rating, reverse=True)
    for movie in sorted_movies:
        print(f"{movie['title']} ({movie['year']}): {movie['rating']}")
    return sorted_movies


def generate_website(MOVIES_FILE, API_KEY):
    with open(MOVIES_FILE, 'r') as newfile:
        movies = json.load(newfile)

    with open('_static/index_template.html', 'r') as fileobj:
        html_template = fileobj.read()

    ADDRESS = f"http://www.omdbapi.com/?apikey={API_KEY}"
    movies_html = ""
    for movie in movies:
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


def main():
    """Main function"""
    with open('movie_storage.json', 'r') as newfile:
        movies = json.load(newfile)
    print("***Welcome to - My Movies Database!***")
    menu()
    user_choice = input("Enter a number (0-9): ")
    while user_choice != '0':
        if user_choice == '1':
            list_movies('movie_storage.json')
        elif user_choice == '2':
            add_movie(movies, API_KEY)
        elif user_choice == '3':
            delete_movie(MOVIES_FILE)
        elif user_choice == '4':
            update_movie(movies)
        elif user_choice == '5':
            stats(movies)
        elif user_choice == '6':
            random_movie(movies)
        elif user_choice == '7':
            search_for_movie(movies)
        elif user_choice == '8':
            sort_movies_by_rating(movies)
        elif user_choice == '9':
            generate_website(MOVIES_FILE, API_KEY)
            print("Website generated successfully!")
        else:
            print("\nInvalid choice!\n")
        menu()
        user_choice = input("Enter a number (0-9): ")
    print("Goodbye!")


if __name__ == "__main__":
    main()
