import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab/english.pickle')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except:
    nltk.download("punkt")
    nltk.download("punkt_tab")
    nltk.download("stopwords")
    nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


def extract_name(text):
    
    if not text:
        return None
    t = text.strip()
    patterns = [
        r"my name is\s+([A-Za-z'-]+)",
        r"call me\s+([A-Za-z'-]+)",
        # avoid feelings: good, fine, great, okay, well, alright
        r"\bi am\s+(?!good\b|fine\b|great\b|okay\b|ok\b|well\b|alright\b)([A-Za-z'-]+)\b",
        r"\bi'm\s+([A-Za-z'-]+)\b",
        r"it's\s+([A-Za-z'-]+)",
    ]
    for p in patterns:
        m = re.search(p, t, flags=re.I)
        if m:
            return m.group(1).capitalize()
    return None


def preprocess_for_intent(text: str) -> str:
   
    if not text:
        return ""

    t = text.lower().strip()
    
    # split words in list
    tokens = word_tokenize(t) 

    # Keep alphabetic tokens and drop stopwords
    tokens = [tok for tok in tokens if tok.isalpha() and tok not in stop_words]

    # Lemmatise
    lemmas = [lemmatizer.lemmatize(tok) for tok in tokens]

    # Join back into string
    return " ".join(lemmas)
