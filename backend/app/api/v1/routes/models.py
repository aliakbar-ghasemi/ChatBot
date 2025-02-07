from fastapi import APIRouter, HTTPException
import subprocess
import json

router = APIRouter()

@router.get("/")
async def get_available_models():
    """
    Fetches and returns a list of available Ollama models.
    """
    try:
        ollama_path = r"C:\Users\Aliakbar\AppData\Local\Programs\Ollama\ollama.exe"
        
        result = subprocess.run([ollama_path, "list"], capture_output=True, text=True)
        models = []
        for line in result.stdout.split("\n")[1:]: # Skip the header
            if line.strip():
                model_name = line.split()[0] # Get the first word as model name
                models.append(model_name)
        return {"models": models}
    
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching models: {e.stderr}")
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse Ollama models response.")
