from transformers import pipeline
from transformers import AutoModelForSequenceClassification

model_name = "facebook/bart-large-mnli"
#model = AutoModelForSequenceClassification.from_pretrained(model_name, force_download=True)

# Load the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model= model_name)

# Define categories
categories = ["Programming", "Machine Learning", "Web Development", "Data Science", "Politics"]

# Function to classify text
def classify_text(text, categories=categories):
    """
    Classifies the given text into one or more categories.
    
    :param text: The long text to classify.
    :param categories: A list of categories (labels) to classify the text into.
    :return: Dictionary of categories with confidence scores.
    """
    # Use the model for zero-shot classification
    result = classifier(text, candidate_labels=categories, multi_label=False)
    
    # Return category scores as a dictionary
    return dict(zip(result["labels"], result["scores"]))


