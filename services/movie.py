from fastapi import HTTPException, status
from models.movie import Movie as MovieModel
from schemas.movie import Movie


class MovieService:
    # Each time this service is called, it should receive a Session to the DB
    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result

    def get_movie(self, id):
        result = self.db.query(MovieModel).where(MovieModel.id == id).first()
        return result

    def get_movie_by_category(self, category):
        result = self.db.query(MovieModel).where(MovieModel.category == category).all()
        return result

    def create_movie(self, movie: Movie):
        # Add received data to model (double asterisk used to unpack values from movie)
        new_movie = MovieModel(**dict(movie))
        # Add the new registry
        self.db.add(new_movie)
        # Make an update, to save changes
        self.db.commit()
        return

    def update_movie(self, id: int, movie: Movie):
        result = self.db.query(MovieModel).where(MovieModel.id == id).first()

        result.title = movie.title
        result.year = movie.year
        result.category = movie.category
        self.db.commit()
        return

    def delete_movie(self, id: int):
        result = self.get_movie(id)
        self.db.delete(result)
        self.db.commit()
        return
