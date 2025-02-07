from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.logger import logger 

class ModelNotFoundException(HTTPException):
    def __init__(self, model_name: str):
        super().__init__(status_code=404, detail=f"Model '{model_name}' not found")

class InvalidRequestException(HTTPException):
    def __init__(self, message: str = "Invalid request"):
        super().__init__(status_code=400, detail=message)

def add_exception_handlers(app: FastAPI):
    """Registers custom exception handlers to the FastAPI app."""
    
    @app.exception_handler(ModelNotFoundException)
    async def model_not_found_handler(request: Request, exc: ModelNotFoundException):
        logger.error(f"Model not found: {exc.detail} | Path: {request.url}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(InvalidRequestException)
    async def invalid_request_handler(request: Request, exc: InvalidRequestException):
        logger.error(f"Invalid request: {exc.detail} | Path: {request.url}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning(f"HTTPException: {exc.detail} | Path: {request.url}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.critical(f"General Exception: {str(exc)} | Path: {request.url}")
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
