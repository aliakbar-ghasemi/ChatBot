from langdetect import detect, DetectorFactory, detect_langs
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
import re

# Ensure deterministic language detection
DetectorFactory.seed = 0

# Download sentence tokenizer if not available
nltk.download('punkt')

def detect_language(text):
    """
    Detects the most probable language from text.
    """
    try:
        lang_probs = detect_langs(text)
        if lang_probs:
            return lang_probs[0].lang  # Get the most probable language
    except:
        return "unknown"
    
def split_by_language(text):
    """
    Splits mixed-language text into separate parts based on detected languages.
    """
    sentences = nltk.sent_tokenize(text)  # Split into sentences
    lang_groups = {}

    for sentence in sentences:
        detected_lang = detect_language(sentence)  # Improved detection

        if detected_lang not in lang_groups:
            lang_groups[detected_lang] = []
        
        lang_groups[detected_lang].append(sentence)

    return lang_groups

def remove_code_blocks(text):
    """
    Removes programming code blocks from the text using regex.
    """
    code_pattern = r"```.*?```|def\s+\w+\(.*?\):.*?\n(?:\s{4}.*\n)*"
    return re.sub(code_pattern, "", text, flags=re.DOTALL)

def summarize_text(text, num_sentences=3):
    """
    Summarizes text by detecting language and applying the appropriate summarization method.
    """
    text = remove_code_blocks(text)  # Remove code before summarization
    lang_parts = split_by_language(text)
    summarized_texts = []

    for language, sentences in lang_parts.items():
        part_text = " ".join(sentences)  # Merge sentences of the same language

        try:
            if language == "unknown":  # If detection fails
                summarized_texts.append(f"[{part_text[:300]}...]")

            else:  # Try Sumy for other languages
                parser = PlaintextParser.from_string(part_text, Tokenizer(language))
                summarizer = LsaSummarizer()
                summary = summarizer(parser.document, num_sentences)
                summarized_texts.append(" ".join(str(sentence) for sentence in summary))

        except Exception as e:
            summarized_texts.append(f"{part_text[:300]}...")

    return "\n---\n".join(summarized_texts)  # Combine summarized parts

# Example mixed-language text with code
mixed_text = """
Python is a powerful programming language used in various fields.
def hello():
    print("Hello, World!")
این یک متن فارسی برای آزمایش خلاصه‌سازی است. خلاصه‌سازی متن به ما کمک می‌کند که سریع‌تر اطلاعات را پردازش کنیم.
Python est un langage de programmation puissant utilisé pour diverses applications.
"""

# Summarize the mixed-language text
summary = summarize_text(mixed_text)
print("Final Summary:\n", summary)
