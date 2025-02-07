from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import ollama
import asyncio
from pydantic import BaseModel
import subprocess
import logging
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

# Allow requests from your Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to "*" to allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

logging.basicConfig(filename="app_errors.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled error: {exc}")  # Save to log file
    return JSONResponse(status_code=500, content={"message": "Something went wrong!"})

# Define request model for JSON body
class ChatRequest(BaseModel):
    prompt: str
    model: str = ""


# Define models and their keywords
MODEL_ROUTES = {
    "llama3": {
        "keywords": [
            "ai",
            "machine learning",
            "deep learning",
            "neural network",
            "help",
            "explain",
        ]
    },
    "codellama:7b": {  # Replaced codellama:34b with codellama:7b
        "keywords": [
            "backend",
            "api",
            "database",
            "server",
            "flask",
            "django",
            "fastapi",
            "asp.net",
            "c#",
        ]
    },
    "codellama:7b": {
        "keywords": [
            "frontend",
            "html",
            "css",
            "javascript",
            "react",
            "vue",
            "angular",
            "typescript",
        ]
    },
    #"starcoder": {
    "deepseek-coder:6.7b": {
        "keywords": ["android", "kotlin", "java", "android studio", "jetpack compose"]
    },
    "mistral": {
        "keywords": [
            "explain",
            "help",
            "what is",
            "how to",
            "ai",
            "machine learning",
            "deep learning",
        ]
    },
    "gemma:7b": {
        "keywords": [
            "chat",
            "conversation",
            "assistant",
            "talk",
            "help me",
            "joke",
            "business",
            "marketing",
            "sales",
            "strategy",
            "finance",
        ]
    },
}

DEFAULT_MODEL = "llama3"


def select_model(prompt: str) -> str:
    """Selects the AI model based on keywords in the prompt."""
    for model_name, data in MODEL_ROUTES.items():
        if any(keyword in prompt.lower() for keyword in data["keywords"]):
            return model_name
    return DEFAULT_MODEL


async def generate_stream(prompt: str, model: str):
    """Streams AI response in real-time."""
    response = ollama.chat(
        model=model, messages=[{"role": "user", "content": prompt}], stream=True
    )

    for message in response:
        yield f"{message['message']['content']}\n\n"
        #await asyncio.sleep(0.01)  # Small delay for smooth streaming



@app.post("/chat", response_class=StreamingResponse)
async def chat_with_ai(request: ChatRequest):
    model = ""
    if(request.model):
        model = request.model
    else:
        model = select_model(request.prompt)  # Select the correct model

    return StreamingResponse(
        generate_stream(request.prompt, model), media_type="application/x-ndjson"
    )

@app.get("/models")
async def get_models():
    try:
        ollama_path = r"C:\Users\Aliakbar\AppData\Local\Programs\Ollama\ollama.exe"
        
        result = subprocess.run([ollama_path, "list"], capture_output=True, text=True)
        models = []
        for line in result.stdout.split("\n")[1:]: # Skip the header
            if line.strip():
                model_name = line.split()[0] # Get the first word as model name
                models.append(model_name)
        return {"models": models}
    except Exception as e:
        return {"error": str(e)}
    
    
@app.get("/")
async def root():
    return {"message": "apps is working!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8062)