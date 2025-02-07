from fastapi import Depends, HTTPException
from app.core.exceptions import ModelNotFoundException
import ollama
from app.core.logger import logger 

def get_available_models():
    """
    Fetches the list of available Ollama models.
    Used to validate model names before processing chat requests.
    """
    try:
        response = ollama.list()
        model_names = [model["model"] for model in response.get("models", [])]
        return model_names
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch models: {str(e)}")

def validate_model(model: str):
    """
    Validates if the requested model exists in the available Ollama models.
    """
    models = get_available_models()  # Get the list of available models
    if model not in models:
        raise ModelNotFoundException(model)
    return model
