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

    def to_dict(self):
        return {
            'title': self.title,
            'year': self.year,
            'rating': self.rating
        }
