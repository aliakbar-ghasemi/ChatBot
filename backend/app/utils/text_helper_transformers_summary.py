from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import os

# Set a new path for the Hugging Face cache
os.environ["TRANSFORMERS_CACHE"] = r"E:\AI\Models\huggingface"
os.environ["HF_HUB_OFFLINE"] = "1"

def chunk_text(text, chunk_size=1024):
    """Splits text into smaller chunks."""
    tokens = tokenizer.encode(text)
    # Ensure we don't exceed the token limit (1024)
    chunks = [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]
    return [tokenizer.decode(chunk) for chunk in chunks]

def summarize_text(text, max_length=700, min_length=20, device=None):
    """
    Summarizes text using Facebook's BART-large-cnn model.
    
    Args:
        text (str): Input text to summarize
        max_length (int): Maximum length of summary (default 700)
        min_length (int): Minimum length of summary (default 20)
        device (int): GPU device ID to use (None for CPU)
    
    Returns:
        str: Generated summary
    """
    # If text is short enough, return it without summarizing
    if len(text) < max_length:
        return text
    
    text = text.replace("\n", " ")
    
    # Set device to GPU or CPU
    device = device if device is not None else 0 if torch.cuda.is_available() else -1
    print(f"Using device: {device}")
    
    model_dir = "E:/AI/Models/huggingface/facebook/bart-large-cnn"
    if not os.path.exists(model_dir):
        raise FileNotFoundError(f"Model files not found at {model_dir}")
    
    model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    
    summarizer = pipeline(
        "summarization", 
        model=model, 
        tokenizer=tokenizer, 
        device=device
    )

    try:
        if not text.strip():
            raise ValueError("Input text cannot be empty")

        # Tokenize the text and check its length
        tokens = tokenizer.encode(text, truncation=True)
        if len(tokens) > 1024:
            print(f"Text has been truncated to 1024 tokens (original length: {len(tokens)})")
            text = tokenizer.decode(tokens[:1024], skip_special_tokens=True)

        # If text exceeds token limit, split it into chunks
        if len(text) > 1024:
            chunks = chunk_text(text, 1024)
            summaries = []

            for chunk in chunks:
                summary = summarizer(
                    chunk,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False,
                    truncation=True,
                    clean_up_tokenization_spaces=True,
                )
                summaries.append(summary[0]["summary_text"])

            # Combine all chunk summaries into one
            return " ".join(summaries).strip()
        
        # Generate summary for the single chunk of text
        summary = summarizer(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
            truncation=True,
            clean_up_tokenization_spaces=True,
        )
        return summary[0]["summary_text"].strip()

    except Exception as e:
        print(f"Summarization failed: {str(e)}")
        return "Fail"

# Example usage
if __name__ == "__main__":
    long_text = """
    سلام کویین 2.5 چه اطلاعاتی راجع به سیم و کابل داری؟


سلام، ممنون از پیام شما.


در مورد سیم و کابل‌ها، آن‌ها در زبان فارسی معمولاً برای به روزرسانی یا حفاظت دستگاه الکترونیکی استفاده می‌شوند. در اینجا چند اطلاعات مهم درباره سیم و کابل‌ها آورده شده است:



سیم‌ها (Wires):



سیم‌ها برای نقل انرژی الکتریکی معمولاً استفاده می‌شوند.

دستگاه‌های مختلفی همچون کامپیوتر، تلویزیون و گوشی معمولاً با سیم‌هایی به اتاق برق متصل می‌شوند.

برخی از سیم‌ها ماده‌ای موصل در داخل دارند که انرژی را به خوبی منتقل می‌کنند.



کابل‌ها (Cables):



کابل‌ها نسبت به سیم‌ها دارای بسته‌بندی جامع‌تر هستند و برای نقل اطلاعات الکترونیکی طراحی شده‌اند.

در صنعت الکترونیک، کابل‌ها برای به روزرسانی دستگاه‌های مختلف مانند سینماتیک، گوشی همراه و موبایل استفاده می‌شوند.

کابل‌های مختلفی وجود دارند مثل کابل‌های USB، HDMI، Ethernet و غیره، هر کدام برای نقل اطلاعات خاصی طراحی شده‌اند.



انتخاب و نصب کابل‌ها:



وقتی یک کابل را خریداری می‌کنید، باید برخی ویژگی‌های آن را در نظر بگیرید، مانند سرعت انتقال داده، طول و انواع موصل.

نصب کابل‌ها نیز به شرح زیر است:

ابتدا مقصد متصل می‌شود.

سپس بخش منابع را با دستگاه رهنمایی کردن فتح و متصل می‌کنید.

سرانجام، موصل‌ها به هم چسبانده می‌شوند و در نهایت کابل را پوشش می‌دهید.





مراقبت از کابل‌ها:



تلاش کنید که کابل‌ها را به صورت منظم و مرتب داشته باشید.

کابل‌ها را از نقرات یا مکان‌های خطرناک مانند زمینه تلفن همراه، دور و دوران فاجعه حفظ کنید.

برای حفاظت از کابل‌ها ممکن است از دستگاه‌هایی مثل پوشش‌کننده یا چراغ‌های نور آبی استفاده کنید.




اگر سوالات خاصی درباره سیم و کابل دارید، لطفاً بپرسید تا بهترین راهنمایی امکان پذیر باشد.
    """
    summary = summarize_text(long_text)
    print(f"Summary: {summary}")
