import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nlp_utils import preprocess_for_intent

faq_questions = []
faq_answers = []
faq_vectorizer = None
faq_matrix = None


def load_faq(csv_path="hospital_faq.csv"):
    global faq_questions, faq_answers, faq_vectorizer, faq_matrix
    try:
        df = pd.read_csv(csv_path)
        if "question" not in df.columns or "answer" not in df.columns:
            faq_questions = []
            faq_answers = []
            faq_vectorizer = None
            faq_matrix = None
            return
        faq_questions = [str(q) for q in df["question"].fillna("")]
        faq_answers = [str(a) for a in df["answer"].fillna("")]
        processed = [preprocess_for_intent(q) for q in faq_questions]
        faq_vectorizer = TfidfVectorizer()
        faq_matrix = faq_vectorizer.fit_transform(processed)
    except Exception:
        faq_questions = []
        faq_answers = []
        faq_vectorizer = None
        faq_matrix = None


load_faq()


def answer_faq(user_text, threshold=0.3):
    global faq_questions, faq_answers, faq_vectorizer, faq_matrix
    if not faq_questions or faq_vectorizer is None or faq_matrix is None:
        return None
    processed = preprocess_for_intent(user_text)
    if not processed:
        return None
    user_vec = faq_vectorizer.transform([processed])
    sims = cosine_similarity(user_vec, faq_matrix).flatten()
    best_idx = int(sims.argmax())
    best_score = float(sims[best_idx])
    if best_score < threshold:
        return None
    return faq_answers[best_idx]
