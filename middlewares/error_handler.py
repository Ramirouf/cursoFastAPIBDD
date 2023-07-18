from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

class ErrorHandler(BaseHTTPMiddleware):
    #Create constructor
    def __init__(self, app:FastAPI) -> None:
        super().__init__(app)

    # Method that detects if an error occurs in the app
    # If no errors occur, call_next will execute the next instruction of the main code
    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        try:
            return await call_next(request)
        except Exception as e:
            return JSONResponse(status_code=500, content={'error': str(e)})