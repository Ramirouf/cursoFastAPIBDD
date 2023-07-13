from fastapi import (
    Depends,
    FastAPI,
    Body,
    Path,
    Query,
    status,
    Response,
    Request,
    HTTPException,
)
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import datetime
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

app = FastAPI(
    title="FastAPI with DB", description="Learning purposes", version="0.0.1"
)
app.title = "My app with FastAPI"
app.version = "0.0.1"

#Create tables
Base.metadata.create_all(bind=engine)


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@gmail.com":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
            )


class User(BaseModel):
    email: str
    password: str


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=20)
    year: int = Field(le=datetime.date.today().year)
    category: str = Field(min_length=5, max_length=20)

    # The following replaces the use of "default" as a parameter in each Field()
    class Config:
        schema_extra = {
            "example": {
                "id": 0,
                "title": "Unknown title",
                "year": 2023,
                "category": "Unknown category",
            }
        }


movies = [
    {"id": 1, "title": "Avatar", "year": 2009, "category": "Action"},
    {"id": 2, "title": "Interstellar", "year": 2014, "category": "Sci-fi"},
]


# "tags" is used to group endpoints in the documentation
@app.get("/", tags=["home"])
def message():
    # return HTMLResponse("<h1>Hello world!</h1>")
    return FileResponse("./index.html")


# Route to allow the user to login
@app.post("/login", tags=["auth"])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=status.HTTP_200_OK, content=token)


# response_model is used to define and document the schema (structure) of the response
@app.get(
    "/movies",
    tags=["movies"],
    response_model=List[Movie],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
)
def get_movies() -> List[Movie]:
    db = Session() # Create a session to connect to DB
    result = db.query(MovieModel).all() # Request all data, using the created model

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
    # Both do the same, because FastAPI by default sends an JSONResponse with the content of the return
    # The following is a redundant way
    # return JSONResponse(content=movies)


@app.get(
    "/movies/{id}",
    tags=["movies"],
    response_model=Movie,
    status_code=status.HTTP_200_OK,
)
# Path is used to validate the path parameter
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).where(MovieModel.id == id).first()
    if result:
        return jsonable_encoder(result)
    else:
        raise HTTPException(status_code=404, detail="Movie not found")


# Query params have key value
@app.get("/movies/", tags=["movies"], response_model=List[Movie])
# Last slash used to declare that a query param will be received
# Filter movies by category
# ↓↓↓ Query is used because a query param is received !!! ↓↓↓
def get_movies_by_category(
    category: str = Query(min_length=5, max_length=15)
) -> List[Movie]:
    # ↑↑↑ FastAPI auto-detects that category is a query param ↑↑↑
    db = Session()
    filteredMovies = db.query(MovieModel).where(MovieModel.category == category).all()
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


@app.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    # Create session to connect to DB
    db = Session()
    # Add received data to model (double asterisk used to unpack values from movie)
    new_movie = MovieModel(**dict(movie))
    # Add the new registry
    db.add(new_movie)
    # Make an update, to save changes
    db.commit()
    #movies.append(dict(movie))
    return {"message": "The movie was registered"}


@app.put("/movies/{id}", tags=["movies"], response_model=dict)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).where(MovieModel.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Movie not found",)
    result.title = movie.title
    result.year = movie.year
    result.category = movie.category
    db.commit()
    return {"message": "The movie was updated"}



@app.delete("/movies/{id}", tags=["movies"], response_model=dict)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).where(MovieModel.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found",)
    db.delete(result)
    db.commit()
    return {"message": "The movie was deleted"}
