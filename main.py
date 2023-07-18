from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import FileResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI(title="FastAPI with DB", description="Learning purposes", version="0.0.1")

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

# Create tables
Base.metadata.create_all(bind=engine)


# "tags" is used to group endpoints in the documentation
@app.get("/", tags=["home"])
def message():
    # return HTMLResponse("<h1>Hello world!</h1>")
    return FileResponse("./index.html")
