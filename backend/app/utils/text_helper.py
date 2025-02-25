from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from gensim.summarization import summarize

DetectorFactory.seed = 0  # Ensures consistent language detection

def extract_main_part(text, max_length=300):
    """Returns the most important part of the text if summarization fails."""
    return text[:max_length] + "..." if len(text) > max_length else text

def summarize_text(text, num_sentences=3):
    try:
        language = detect(text)  # Detect the dominant language
    except LangDetectException:
        language = "unknown"

    # Persian (fa) - Use Sumy
    if language == "fa":
        try:
            parser = PlaintextParser.from_string(text, Tokenizer("persian"))
            summarizer = LsaSummarizer()
            summary = summarizer(parser.document, num_sentences)
            return ' '.join([str(sentence) for sentence in summary])
        except:
            return extract_main_part(text)

    # English (en) or Programming Code - Use Gensim
    elif language == "en":
        try:
            summary = summarize(text, ratio=0.3)
            return summary if summary else extract_main_part(text)
        except:
            return extract_main_part(text)

    # Mixed or Unsupported Language - Fallback to Main Part
    else:
        try:
            parser = PlaintextParser.from_string(text, Tokenizer(language))
            summarizer = LsaSummarizer()
            summary = summarizer(parser.document, num_sentences)
            return ' '.join([str(sentence) for sentence in summary])
        except:
            return f"⚠️ Mixed or unsupported language detected ({language}). Returning main part:\n{extract_main_part(text)}"

# Example Texts
persian_text = "این یک متن فارسی برای آزمایش خلاصه‌سازی است. خلاصه‌سازی متن به ما کمک می‌کند که سریع‌تر اطلاعات را پردازش کنیم."
english_text = "Python is a powerful programming language used for various applications. It supports multiple programming paradigms.\ndef hello():\n    print('Hello, World!')\nThis function prints Hello, World! on the screen."
mixed_text = "این متن شامل Persian and English sentences mixed together. خلاصه‌سازی یک روش خوب است. Python is also a great language."

# Test Summarization
print("Persian Summary:", summarize_text(persian_text))
print("English Summary:", summarize_text(english_text))
print("Mixed Summary:", summarize_text(mixed_text))
