class MovieApp:
  def __init__(self, storage):
    self._storage = storage

  def _command_list_movies(self):
    movies = self._storage.list_movies()

  def _command_movie_stats(self):
    pass

  def _generate_website(self):
    pass

  def run(self):
    pass