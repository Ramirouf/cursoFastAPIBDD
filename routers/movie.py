from fastapi import APIRouter
from fastapi import (
    Depends,
    Path,
    Query,
    status,
    HTTPException,
)
from fastapi.responses import JSONResponse
from pydantic import Field
from typing import List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


# response_model is used to define and document the schema (structure) of the response
@movie_router.get(
    "/movies",
    tags=["movies"],
    response_model=List[Movie],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
)
def get_movies() -> List[Movie]:
    db = Session()  # Create a session to connect to DB
    result = MovieService(db).get_movies()  # Request all data, using the created model

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(result)
    )
    # Both do the same, because FastAPI by default sends an JSONResponse with the content of the return
    # The following is a redundant way
    # return JSONResponse(content=movies)


@movie_router.get(
    "/movies/{id}",
    tags=["movies"],
    response_model=Movie,
    status_code=status.HTTP_200_OK,
)
# Path is used to validate the path parameter
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if result:
        return jsonable_encoder(result)
    else:
        raise HTTPException(status_code=404, detail="Movie not found")


# Query params have key value
@movie_router.get("/movies/", tags=["movies"], response_model=List[Movie])
# Last slash used to declare that a query param will be received
# Filter movies by category
# ↓↓↓ Query is used because a query param is received !!! ↓↓↓
def get_movies_by_category(
    category: str = Query(min_length=5, max_length=15)
) -> List[Movie]:
    # ↑↑↑ FastAPI auto-detects that category is a query param ↑↑↑
    db = Session()
    filteredMovies = MovieService(db).get_movie_by_category(category)
    if filteredMovies:
        return filteredMovies
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found for the given category",
        )
    # for item in movies:
    #     if item["category"] == category and item["year"] == year:
    #         return item
    # return []


@movie_router.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    # Create session to connect to DB
    db = Session()
    MovieService(db).create_movie(movie)
    return {"message": "The movie was registered"}


@movie_router.put("/movies/{id}", tags=["movies"], response_model=dict)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )
    MovieService(db).update_movie(id, movie)
    return {"message": "The movie was updated"}


@movie_router.delete("/movies/{id}", tags=["movies"], response_model=dict)
def delete_movie(id: int) -> dict:
    db = Session()
    MovieService(db).delete_movie(id)
    return {"message": "The movie was deleted"}
