import ollama
from app.core.logger import logger
#from app.utils.text_helper import summarize_text
from app.utils.text_helper_transformers import classify_text
import json

# AI model categories mapped to the best models
MODEL_CATEGORIES = [
  {
    "id": 1,
    "category": "General Language Understanding",
    "model": "llama3:8b"
  },
  {
    "id": 2,
    "category": "Conversational AI (Chatbots, Assistants)",
    "model": "llama3:8b"
  },
  {
    "id": 3,
    "category": "English Learning & Fluency",
    "model": "mistral:7b"
  },
  {
    "id": 4,
    "category": "Python Development",
    "model": "deepseek-coder:6.7b"
  },
  {
    "id": 5,
    "category": "ASP.NET Core & Backend Development",
    "model": "deepseek-coder:6.7b"
  },
  {
    "id": 6,
    "category": "Frontend Development (Vue, Angular, React)",
    "model": "deepseek-coder:6.7b"
  },
  {
    "id": 7,
    "category": "Android Development (Java/Kotlin)",
    "model": "deepseek-coder:6.7b"
  },
  {
    "id": 8,
    "category": "Data Science & AI Development",
    "model": "mistral:7b"
  },
  {
    "id": 9,
    "category": "Mathematical & Logical Reasoning",
    "model": "mistral:7b"
  },
  {
    "id": 10,
    "category": "Creative Writing & Storytelling",
    "model": "mistral:7b"
  },
  {
    "id": 11,
    "category": "Scientific & Research Analysis",
    "model": "llama3:8b"
  },
  {
    "id": 12,
    "category": "Medical & Healthcare AI",
    "model": "meditron:7b"
  },
  {
    "id": 13,
    "category": "Finance, Business & Economics",
    "model": "gemma:7b"
  },
  {
    "id": 14,
    "category": "Cybersecurity & Threat Detection",
    "model": "falcon:7b"
  },
]

# Mistral 7B prompt for classification
CLASSIFICATION_PROMPT = """
You are a classification expert. Analyze the user’s input and map it to **ONE** of the 14 categories below.  

**Categories**:  
1. General Language Understanding  
2. Conversational AI  
3. English Learning & Fluency  
4. Python Development  
5. ASP.NET Core & Backend Development  
6. Frontend Development  
7. Android Development  
8. Data Science & AI Development  
9. Mathematical & Logical Reasoning  
10. Creative Writing & Storytelling  
11. Scientific & Research Analysis  
12. Medical & Healthcare AI  
13. Finance, Business & Economics  
14. Cybersecurity & Threat Detection  

**Rules**:  
- Return **ONLY** the JSON format: `{"id": X, "category": "Category Name"}`.  
- Choose the **MOST SPECIFIC** category (e.g., "debug Kotlin code" → `7`, not `1`).  
- For ambiguous inputs, use this priority:  
  Technical domains (4-14) > General/Creative (1-3, 9-10).  
- If input fits **multiple categories**, pick the one mentioned **first** in this list.  

**Examples**:  
Input: "How to handle CORS in ASP.NET Core?"  
Output: `{"id": 5, "category": "ASP.NET Core & Backend Development"}`  

Input: "Is this sentence grammatically correct?"  
Output: `{"id": 3, "category": "English Learning & Fluency"}`  

Input: "Write a sci-fi story about AI rebellion."  
Output: `{"id": 10, "category": "Creative Writing & Storytelling"}`  

Input: "Calculate the eigenvalues of this matrix."  
Output: `{"id": 9, "category": "Mathematical & Logical Reasoning"}`  

**Critical Notes**:  
- Never add explanations.  
- Never invent new categories.  
- If completely unrelated (e.g., "hello"), use `{"id": 1, "category": "General Language Understanding"}`.  
"""


def classify_prompt(user_prompt):
    """Classifies the user prompt using Mistral 7B."""
    # content = CLASSIFICATION_PROMPT.format(user_prompt=user_prompt)
    try:
        response = ollama.chat(
            #model="mistral:7b",
            #model="gemma:2b",
            model="llama3:8b",
            messages=[
                {"role": "system", "content": CLASSIFICATION_PROMPT},
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            options={"temperature": 0},  # Ensure deterministic output
        )
        category = response["message"]["content"].strip()
        parsed_category = json.loads(category)
        logger.info(f"🧠 Category Detected: {parsed_category}")
        
        # Convert list to {id: item} dictionary
        id_to_item = {item["id"]: item for item in MODEL_CATEGORIES}
        result = id_to_item.get(parsed_category['id'])
        
        if result:
            return result["model"]
        else:
            return MODEL_CATEGORIES[0]["model"]
        
    except Exception as e:
        logger.error(f"Classification failed: {e}")
        return MODEL_CATEGORIES[0]["model"]


def select_model(user_prompt: str) -> str:
    """Route user prompt to the best AI model."""
    logger.info(f"🚀 select_model: Routing user prompt to the best AI model...")
    #summary = summarize_text(user_prompt)
    
    #categories = [item["category"] for item in MODEL_CATEGORIES]
    #classification_result = classify_text(user_prompt, categories)
    
    selected_model = classify_prompt(user_prompt)
    logger.info(f"🚀 Routing to model: {selected_model}")

    return selected_model
