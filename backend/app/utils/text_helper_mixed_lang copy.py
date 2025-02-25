from langdetect import detect, DetectorFactory, detect_langs
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from gensim.summarization import summarize
import nltk
import re

# Ensure deterministic language detection
DetectorFactory.seed = 0

# Download sentence tokenizer if not already available
#nltk.download('punkt')

def split_by_language(text):
    """
    Splits mixed-language text into separate parts based on detected languages.
    """
    sentences = nltk.sent_tokenize(text)  # Split into sentences
    lang_groups = {}

    for sentence in sentences:
        try:
            detected_lang = detect(sentence)
        except:
            detected_lang = "unknown"

        if detected_lang not in lang_groups:
            lang_groups[detected_lang] = []
        
        lang_groups[detected_lang].append(sentence)

    return lang_groups

def summarize_text(text, num_sentences=3):
    """
    Summarizes text by detecting language and applying the appropriate summarization method.
    """
    lang_parts = split_by_language(text)
    summarized_texts = []

    for language, sentences in lang_parts.items():
        part_text = " ".join(sentences)  # Merge sentences of the same language

        if language == "fa":  # Persian (use Sumy)
            parser = PlaintextParser.from_string(part_text, Tokenizer("persian"))
            summarizer = LsaSummarizer()
            summary = summarizer(parser.document, num_sentences)
            summarized_texts.append(" ".join(str(sentence) for sentence in summary))

        elif language == "en":  # English (use Gensim)
            try:
                summary = summarize(part_text, ratio=0.3)  # Adjust ratio as needed
                summarized_texts.append(summary)
            except:
                summarized_texts.append(part_text)

        elif language == "unknown":  # If detection fails
            summarized_texts.append(f"[{part_text[:300]}...]")

        else:  # Try Sumy for other languages
            try:
                parser = PlaintextParser.from_string(part_text, Tokenizer(language))
                summarizer = LsaSummarizer()
                summary = summarizer(parser.document, num_sentences)
                summarized_texts.append(" ".join(str(sentence) for sentence in summary))
            except:
                summarized_texts.append(part_text)

    return "\n---\n".join(summarized_texts)  # Combine summarized parts

# Example mixed-language text
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
