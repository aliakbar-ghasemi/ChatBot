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
    "deepseek-coder:6.7b": {  
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
    "starcoder:latest": {
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
    "codellama:13b": {
        "keywords": ["android", "kotlin", "java", "android studio", "jetpack compose"]
    },
    "mistral:latest": {
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

DEFAULT_MODEL = "llama3:latest"

def select_model(prompt: str) -> str:
    """Selects the AI model based on keywords in the prompt."""
    for model_name, data in MODEL_ROUTES.items():
        if any(keyword in prompt.lower() for keyword in data["keywords"]):
            return model_name
    return DEFAULT_MODEL