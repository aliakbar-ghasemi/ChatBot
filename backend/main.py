from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import chat, models, conversations
from app.core.config import settings
from app.core.exceptions import add_exception_handlers
from app.core.logger import logger

# Initialize FastAPI app
app = FastAPI(title=settings.APP_NAME, version=settings.API_VERSION)

# Add Global Exception Handlers
add_exception_handlers(app)

# Enable CORS (Allow frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(chat.router, prefix=f"/api/{settings.API_VERSION}/chat", tags=["chat"])
app.include_router(conversations.router, prefix=f"/api/{settings.API_VERSION}/conversations", tags=["conversations"])
app.include_router(models.router, prefix=f"/api/{settings.API_VERSION}/models", tags=["models"])

logger.info("🚀 FastAPI Server Started...")

# Root Endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Chatbot API!"}


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server...")
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
